from contextvars import ContextVar

# Define a ContextVar to hold tenant configuration
tenant_context: ContextVar[dict] = ContextVar("tenant_context", default={})