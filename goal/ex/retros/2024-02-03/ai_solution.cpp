/// user.cpp ///
const int MAX_DEVICE = 256;
const int MAX_ROOM = 52;

struct DetectedDevice
{
	int id;
	int power;
	int tx;
	int ty;
};

extern int scan_device(int mDeviceId, int mScanPower, DetectedDevice mDetected[]);

#define ABS_VAL(x) ((x) < 0 ? -(x) : (x))

static const int SCAN_POWER = 380;

static int gDeviceCount;
static int gDeviceIds[MAX_DEVICE];
static unsigned char gScanned[MAX_DEVICE];
static unsigned char gAdj[MAX_DEVICE][MAX_DEVICE];

static int gRoomCount;
static int gRoomDeviceCount[MAX_ROOM];
static int gRoomDeviceIds[MAX_ROOM][MAX_DEVICE];
static unsigned char gRoomsPrepared;

static int ensure_device_index(int deviceId, int* isNew)
{
	for (int i = 0; i < gDeviceCount; ++i)
	{
		if (gDeviceIds[i] == deviceId)
		{
			if (isNew)
				*isNew = 0;
			return i;
		}
	}

	if (gDeviceCount >= MAX_DEVICE)
		return -1;

	int idx = gDeviceCount++;
	gDeviceIds[idx] = deviceId;
	gScanned[idx] = 0;
	if (isNew)
		*isNew = 1;
	return idx;
}

static int is_clear_path(int scanPower, int tx, int ty, int power)
{
	int spent = scanPower - power;
	int manhattan = ABS_VAL(tx) + ABS_VAL(ty);
	return spent == manhattan;
}

static void sort_int_array(int* data, int size)
{
	for (int i = 1; i < size; ++i)
	{
		int key = data[i];
		int j = i - 1;
		while (j >= 0 && data[j] > key)
		{
			data[j + 1] = data[j];
			--j;
		}
		data[j + 1] = key;
	}
}

static void sort_rooms()
{
	for (int i = 0; i < gRoomCount; ++i)
	{
		for (int j = i + 1; j < gRoomCount; ++j)
		{
			int firstI = gRoomDeviceIds[i][0];
			int firstJ = gRoomDeviceIds[j][0];
			if (firstJ < firstI)
			{
				int tempCount = gRoomDeviceCount[i];
				gRoomDeviceCount[i] = gRoomDeviceCount[j];
				gRoomDeviceCount[j] = tempCount;

				for (int k = 0; k < MAX_DEVICE; ++k)
				{
					int tempValue = gRoomDeviceIds[i][k];
					gRoomDeviceIds[i][k] = gRoomDeviceIds[j][k];
					gRoomDeviceIds[j][k] = tempValue;
				}
			}
		}
	}
}

static void prepare_rooms()
{
	if (gRoomsPrepared)
		return;

	int visited[MAX_DEVICE];
	for (int i = 0; i < gDeviceCount; ++i)
		visited[i] = 0;

	gRoomCount = 0;
	for (int i = 0; i < gDeviceCount; ++i)
	{
		if (visited[i])
			continue;

		int stack[MAX_DEVICE];
		int top = 0;
		stack[top++] = i;
		visited[i] = 1;

		int collected[MAX_DEVICE];
		int cCount = 0;

		while (top > 0)
		{
			int current = stack[--top];
			collected[cCount++] = gDeviceIds[current];

			for (int j = 0; j < gDeviceCount; ++j)
			{
				if (gAdj[current][j] && !visited[j])
				{
					visited[j] = 1;
					stack[top++] = j;
				}
			}
		}

		sort_int_array(collected, cCount);

		for (int k = 0; k < cCount; ++k)
			gRoomDeviceIds[gRoomCount][k] = collected[k];

		for (int k = cCount; k < MAX_DEVICE; ++k)
			gRoomDeviceIds[gRoomCount][k] = 0;

		gRoomDeviceCount[gRoomCount] = cCount;
		++gRoomCount;
	}

	if (gRoomCount > 1)
		sort_rooms();

	gRoomsPrepared = 1;
}

static void reset_state(int initialDeviceId)
{
	gDeviceCount = 0;
	gRoomsPrepared = 0;
	for (int i = 0; i < MAX_DEVICE; ++i)
	{
		gDeviceIds[i] = 0;
		gScanned[i] = 0;
		for (int j = 0; j < MAX_DEVICE; ++j)
			gAdj[i][j] = 0;
	}

	int isNew = 0;
	ensure_device_index(initialDeviceId, &isNew);
}

void scan(int mDeviceId, int mTotalDevice)
{
	reset_state(mDeviceId);
	if (mTotalDevice <= 0)
		return;

	DetectedDevice detected[MAX_DEVICE];
	int queue[MAX_DEVICE];
	int front = 0;
	int back = 0;
	queue[back++] = 0;

	while (front < back)
	{
		int idx = queue[front++];
		if (gScanned[idx])
			continue;

		gScanned[idx] = 1;

		int numDetected = scan_device(gDeviceIds[idx], SCAN_POWER, detected);
		if (numDetected <= 0)
			continue;

		for (int i = 0; i < numDetected; ++i)
		{
			int isNew = 0;
			int neighborIdx = ensure_device_index(detected[i].id, &isNew);
			if (neighborIdx == -1)
				continue;

			if (isNew && back < MAX_DEVICE)
				queue[back++] = neighborIdx;

			if (is_clear_path(SCAN_POWER, detected[i].tx, detected[i].ty, detected[i].power))
			{
				gAdj[idx][neighborIdx] = 1;
				gAdj[neighborIdx][idx] = 1;
			}
		}

	}
}

void result(int mDeviceIds[][MAX_DEVICE])
{
	prepare_rooms();

	for (int i = 0; i < gRoomCount; ++i)
	{
		int count = gRoomDeviceCount[i];
		for (int j = 0; j < count; ++j)
			mDeviceIds[i][j] = gRoomDeviceIds[i][j];
		for (int j = count; j < MAX_DEVICE; ++j)
			mDeviceIds[i][j] = 0;
	}

	for (int i = gRoomCount; i < MAX_ROOM; ++i)
		for (int j = 0; j < MAX_DEVICE; ++j)
			mDeviceIds[i][j] = 0;
}

