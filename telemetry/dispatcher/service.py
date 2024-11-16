import logging
from datetime import datetime

import grpc
from pymongo.collection import Collection

from core.database import get_collection
from dispatcher.dispatcher_pb2 import Response, AverageResponse, LastRecordResponse, DeviceData  # noqa
from dispatcher.dispatcher_pb2_grpc import DispatcherServicer
from dispatcher.utils import get_time_range

logger = logging.getLogger(__name__)


class DispatcherGRPCService(DispatcherServicer):
    def __init__(self, collection: Collection):
        self.collection = collection

    def GetDataForPeriod(self, request, context):
        try:
            mac_address = request.mac_address
            start_time, end_time = get_time_range(request.start_time, request.end_time)

            query = {
                "mac_address": mac_address,
                "timestamp": {
                    "$gte": start_time.isoformat(),
                    "$lte": end_time.isoformat()
                }
            }
            data = list(self.collection.find(query))

            return Response(
                status="success",
                message="Data fetched successfully",
                data=str(data)  # Ensure str(data) or serialize properly
            )
        except Exception as e:
            logger.error(f"Error fetching data for period: {e}")
            return Response(
                status="error",
                message=f"Error fetching data: {str(e)}",
                data=""
            )

    def GetAverageData(self, request, context):
        try:
            mac_address = request.mac_address
            start_time, end_time = get_time_range(request.start_time, request.end_time)

            pipeline = [
                {
                    "$match": {
                        "mac_address": mac_address,
                        "timestamp": {
                            "$gte": start_time.isoformat(),
                            "$lte": end_time.isoformat()
                        }
                    }
                },
                {
                    "$group": {
                        "_id": None,
                        "avg_temperature": {"$avg": "$temperature"},
                        "avg_humidity": {"$avg": "$humidity"}
                    }
                }
            ]
            result = list(self.collection.aggregate(pipeline))

            if result:
                avg_temperature = result[0].get("avg_temperature", 0.0)
                avg_humidity = result[0].get("avg_humidity", 0.0)
                return AverageResponse(
                    status="success",
                    message="Average data calculated successfully",
                    avg_temperature=avg_temperature,
                    avg_humidity=avg_humidity
                )
            else:
                return AverageResponse(
                    status="error",
                    message="No data found in the specified period",
                    avg_temperature=0.0,
                    avg_humidity=0.0
                )
        except Exception as e:
            logger.error(f"Error calculating average data: {e}")
            return AverageResponse(
                status="error",
                message=f"Error calculating average: {str(e)}",
                avg_temperature=0.0,
                avg_humidity=0.0
            )

    def GetLastRecord(self, request, context):
        try:
            mac_address = request.mac_address
            query = {"mac_address": mac_address}

            last_record = self.collection.find_one(
                filter=query,
                sort=[("timestamp", -1)]
            )

            if last_record:
                return LastRecordResponse(
                    status="success",
                    message="Last record fetched successfully",
                    last_record=DeviceData(
                        id=str(last_record.get("_id", "")),
                        mac_address=last_record.get("mac_address", ""),
                        temperature=float(last_record.get("temperature", 0.0) or 0.0),
                        humidity=float(last_record.get("humidity", 0.0) or 0.0),
                        pressure=float(last_record.get("pressure", 0.0) or 0.0),
                        soil_moisture=float(last_record.get("soil_moisture", 0.0) or 0.0),
                        timestamp=str(last_record.get("timestamp", ""))
                    )
                )
            else:
                context.set_details("No record found for given MAC address.")
                context.set_code(grpc.StatusCode.NOT_FOUND)
                return LastRecordResponse(
                    status="error",
                    message="No data found",
                    last_record=DeviceData()
                )
        except Exception as e:
            logger.error(f"Error fetching last record: {e}")
            context.set_details(f"Error fetching last record: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return LastRecordResponse(
                status="error",
                message=f"Error fetching last record: {str(e)}",
                last_record=DeviceData()
            )
