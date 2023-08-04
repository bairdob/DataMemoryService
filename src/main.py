import traceback
import uuid

from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from models import PointDao, Point, TableView

app = FastAPI()

data = PointDao()
data.generate_data()


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
    error_response = {
        'message': str(exc),
        'traceback': traceback.format_exc(),
        'url': request.url._url,
    }
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response
    )


@app.get("/table")
async def read_rows(view: TableView) -> JSONResponse:
    """
    Reads rows from the data source on the specified view parameters.

    :param view: View contains the offset and limit parameters.
    :return: A JSON response with the requested data and metadata.
    """
    points, size = data.read(offset=view.offset, limit=view.limit)

    rows = [
        Point(x=points[index].x, y=points[index].y, id=str(uuid.UUID(bytes=bytes(points[index].id))))
        for index, point in enumerate(points)
    ]

    return {"data": rows, "metadata": {"size": size, "offset": view.offset, "limit": view.limit}}
