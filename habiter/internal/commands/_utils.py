"""
The methods provided here were deleted but the modules should still exist
in case of methods needed that are specific to the cli commands 
"""


def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()
