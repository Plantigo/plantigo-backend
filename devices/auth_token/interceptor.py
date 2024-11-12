import grpc
from fastapi import HTTPException
from auth_token.services import verify_token


class AuthInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        metadata = dict(handler_call_details.invocation_metadata)
        auth_token = metadata.get("authorization")

        if not auth_token or not auth_token.startswith("Bearer "):
            return grpc.unary_unary_rpc_method_handler(
                lambda request, context: context.abort(grpc.StatusCode.UNAUTHENTICATED, "Unauthenticated"))

        token = auth_token.split(" ")[1]

        try:
            token_data = verify_token(token)
        except HTTPException as e:
            return grpc.unary_unary_rpc_method_handler(
                lambda request, context: context.abort(grpc.StatusCode.UNAUTHENTICATED, "Unauthenticated"))

        return continuation(handler_call_details)
