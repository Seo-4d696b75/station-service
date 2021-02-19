import math

class LatLng:
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

class StationNode(LatLng):
    def __init__(self,depth,data,data_map):
        super().__init__(data['lat'], data['lng'])
        self.depth = depth
        self.code = data['code']
        self.right = None
        self.left = None
        left = data.get('left')
        if left is not None:
            self.left = StationNode(self.depth+1,data_map[left],data_map)
        right = data.get('right')
        if right is not None:
            self.right = StationNode(self.depth+1,data_map[right],data_map)

    def release(self):
        if self.left is not None:
            self.left.release()
        if self.right is not None:
            self.right.release()
        self.left = None
        self.right = None

SPHERE_RADIUS = 6371009.0

def measure(p1, p2, sphere=False):
    if sphere:
        lng1 = math.pi * p1.lng / 180
        lat1 = math.pi * p1.lat / 180
        lng2 = math.pi * p2.lng / 180
        lat2 = math.pi * p2.lat / 180
        lng = (lng1 - lng2)/2
        lat = (lat1 - lat2)/2
        return SPHERE_RADIUS * 2 * math.asin(math.sqrt(math.pow(math.sin(lat),2) + math.cos(lat1) * math.cos(lat2) * math.pow(math.sin(lng),2)))
    else:
        lat = p1.lat - p2.lat
        lng = p1.lng - p2.lng
        return math.sqrt(lat*lat + lng*lng) 

def distance_to_longitude(pos, lng):
    lng = math.pi * abs(pos.lng - lng) / 180
    lat = math.pi * pos.lat / 180
    return SPHERE_RADIUS * math.asin(math.sin(lng) * math.cos(lat))

class KdTree:

    def __init__(self,data):
        map = {}
        for e in data['node_list']:
            map[e['code']] = e
        self.root = StationNode(0, map[data['root']], map)

    def release(self):
        if self.root is not None:
            self.root.release()

    def search_nearest(self, lat, lng, k=1, r=0, sphere=False):
        if k < 1 or self.root is None:
            return []
        else:
            dst = []
            self.search(self.root, LatLng(lat, lng), k, r, dst, sphere)
            return dst

    def search(self, node, pos, k, r, dst, sphere):
        d = measure(pos, node, sphere)
        index = -1
        size = len(dst)
        if size > 0 and d < dst[size-1]['dist']:
            index = size - 1
            while index > 0:
                if d >= dst[index-1]['dist']:
                    break
                index -= 1
        elif size == 0:
            index = 0
        if index >= 0:
            dst.insert(index, {'dist':d, 'code':node.code})
            if size >= k and dst[size]['dist'] > r:
                dst.pop(size)
        x = (node.depth % 2 == 0)
        value = pos.lng if x else pos.lat
        threshold = node.lng if x else node.lat
        next = node.left if value < threshold else node.right
        if next is not None:
            self.search(next, pos, k, r, dst, sphere)
        next = node.right if value < threshold else node.left
        dist2th = abs(value - threshold)
        if sphere and x:
            dist2th = distance_to_longitude(pos, threshold)
        elif sphere and not x:
            dist2th = SPHERE_RADIUS * math.pi * abs(value - threshold) / 180
        if next is not None and dist2th < max(dst[-1]['dist'], r):
            self.search(next, pos, k, r, dst, sphere)


