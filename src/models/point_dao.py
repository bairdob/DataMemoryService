import ctypes
import uuid

DATA_PATH = 'data.bin'
POINTS_AMOUNT = 5


class PointStructure(ctypes.Structure):
    """
    Represents a point in a 2-dimensional space.

    Attributes:
    -----------
        x (int): The x-coordinate of the point.
        y (int): The y-coordinate of the point.
        id (ctypes.c_ubyte * 16): The unique ID of the point.
    """
    _pack_ = 1
    _fields_ = [('x', ctypes.c_int),
                ('y', ctypes.c_int),
                ('id', ctypes.c_ubyte * 16)]

    def __repr__(self):
        return f'Point(x={self.x}, y={self.y}, id={uuid.UUID(bytes=bytes(self.id))})'

    @classmethod
    def sizeof(cls):
        return ctypes.sizeof(cls)


class PointDao:
    """
    Class is responsible for handling operations related to storing and retrieving Point objects.
    """
    points = []
    mem_view: memoryview = ...

    def generate_data(self, amount: int = POINTS_AMOUNT) -> None:
        """
        Generates random points and stores them in the class instance and load to memory view.

        :param amount: The number of points to generate.
        """
        self.points = [PointStructure(i, i, (ctypes.c_ubyte * 16)(*uuid.uuid4().bytes)) for i in range(amount)]

        points_array = bytearray()
        for point in self.points:
            points_array.extend(bytearray(ctypes.string_at(ctypes.addressof(point), ctypes.sizeof(point))))

        self.mem_view = memoryview(points_array)

    def save(self, file_path: str = DATA_PATH):
        """
        Saves memory view as bytesarray to file.

        :param file_path: File path
        """
        with open(file_path, "wb") as f:
            f.write(self.mem_view)

    def load(self, file_path: str = DATA_PATH):
        """
        Reading data from a file and initialize the points list and memoryview.

        :param file_path: File path.
        """
        with open(file_path, 'rb') as f:
            raw_data = bytearray(f.read())
        self.mem_view = memoryview(raw_data)

        self.points = []  # Clear the points list
        for point_index in range(int(len(self.mem_view) / PointStructure.sizeof())):
            offset = point_index * PointStructure.sizeof()
            point_data = self.mem_view[offset: offset + PointStructure.sizeof()]
            buffer = ctypes.create_string_buffer(point_data.tobytes())
            point = ctypes.cast(buffer, ctypes.POINTER(PointStructure)).contents
            self.points.append(point)

    def read(self, offset: int = 0, limit: int = 0):
        """
        Reads points from the memory view.

        :param offset: The starting index to read the points.
        :param limit: The maximum number of points to read.
        :return: Tuple containing a list of Point objects and the total number of points available.
        """
        points_amount = int(len(self.mem_view) / PointStructure.sizeof())

        limit = min(points_amount - offset, limit or points_amount)

        points = []
        for index in range(offset, offset + limit):
            offset = index * PointStructure.sizeof()
            # Read the Point object at the specified offset
            point_data = self.mem_view[offset: offset + PointStructure.sizeof()]
            # Create buffer from the byte array
            buffer = ctypes.create_string_buffer(point_data.tobytes())
            # Cast the buffer to a Point instance
            point: PointStructure = ctypes.cast(buffer, ctypes.POINTER(PointStructure)).contents
            points.append(point)

        return points, points_amount


if __name__ == "__main__":
    data = PointDao()
    # data.generate_data()
    # data.save()
    data.load()

    points = data.read(1, 2)
    # points = data.read()
    for point in points[0]:
        print(point)
