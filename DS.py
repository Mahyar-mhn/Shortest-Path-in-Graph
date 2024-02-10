class Interval:
    def __init__(self, a, b, weight):
        self.a = a
        self.b = b
        self.weight = weight
        self.successor = None
        self.Parent = None
        self.isActive = True
        self.pathSize = -1
        self.representative = None


class Pair:
    def __init__(self, point, interval, Start):
        self.point = point
        self.interval = interval
        self.Start = Start


def Bucket(intervals, n):
    sortedIntervals = [None] * n
    FinalArray = []
    for interval in intervals:
        sortedIntervals[interval.b] = interval
    for interval in sortedIntervals:
        if interval is not None:
            FinalArray.append(interval)
    return FinalArray


def BucketSort(containers, n):
    FinalArray = []
    SortedIntervals = [None] * n
    for container in containers:
        SortedIntervals[container.point] = container
    for container in SortedIntervals:
        if container is not None:
            FinalArray.append(container)
    return FinalArray



def reverse_list(lst):
    return lst[::-1]


def setSuccessor(containers):
    reversed_container = reverse_list(containers)
    last_seen = None
    for container in reversed_container:
        if not container.Start:
            last_seen = container.interval
        else:
            container.interval.successor = last_seen


def Find(x):
    p = Parents[sortedIntervals.index(x)]
    if p == x:
        return x
    Parents[sortedIntervals.index(x)] = Find(p)
    return Parents[sortedIntervals.index(x)]


def Union(x, y):
    rootX = Find(x)
    rootY = Find(y)
    if rootY == rootX:
        return False
    if size[sortedIntervals.index(rootY)] > size[sortedIntervals.index(rootX)]:
        rootX, rootY = rootY, rootX
    Parents[sortedIntervals.index(rootY)] = rootX
    newSize = size[sortedIntervals.index(rootX)] + size[sortedIntervals.index(rootY)]
    size[sortedIntervals.index(rootX)] = newSize
    return True


Parents = []
size = []
sortedIntervals = []

if __name__ == "__main__":
    containers = []
    Actives = []
    InActives = []

    n = int(input())
    if n == 0:
        exit()

    for _ in range(n):
        a, end, weight = map(int, input().split())
        interval = Interval(a, end, weight)
        containers.append(Pair(a, interval, True))
        containers.append(Pair(end, interval, False))
        sortedIntervals.append(interval)

    sortedIntervals = Bucket(sortedIntervals, 100000)
    containers = BucketSort(containers, 100000)
    setSuccessor(containers)

    for interval in sortedIntervals:
        Parents.append(interval)
        size.append(1)

    i = 0
    sortedIntervals[0].pathSize = sortedIntervals[0].weight
    Actives.append(sortedIntervals[i])
    sortedIntervals[0].Parent = sortedIntervals[0]

    for i in range(1, len(sortedIntervals)):
        interval = sortedIntervals[i]
        if Find(interval.successor) == interval:
            interval.isActive = False
            InActives.append(interval)
        elif Find(interval.successor).isActive:
            interval.pathSize = Find(interval.successor).Parent.pathSize + interval.weight
            while interval.pathSize < Actives[-1].pathSize:
                Union(interval, Actives.pop())
                Find(interval).Parent = interval
            while InActives:
                Union(interval, InActives.pop())
            Actives.append(interval)
        elif not Find(interval.successor).isActive:
            Union(Find(interval.successor), interval)

    for interval in sortedIntervals:
        if interval.pathSize == -1 and Find(interval).Parent is not None:
            interval.pathSize = interval.weight + Find(interval).Parent.pathSize

    for i, interval in enumerate(sortedIntervals, 1):
        print(i, interval.pathSize)
