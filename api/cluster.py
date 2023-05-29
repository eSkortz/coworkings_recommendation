from typing import List
from coworking import Coworking, CoworkingId
from .recommender import Recommender
import numpy as np

class ClusteringRecommender(Recommender):
    def __init__(self, data: List[Coworking]):
        # get all tags from all coworkings
        all_tags = set([ tag.id for coworking in data for tag in coworking.tags ])

        # convert coworkings to vectors
        # if a coworking has a tag, then the corresponding element in the vector is 1, otherwise 0
        def coworking_to_tags_vec(coworking: Coworking):
            vec = []

            coworking_tags = set([ tag.id for tag in coworking.tags ])
            for tag in all_tags:
                if tag in coworking_tags:
                    vec.append(1)
                else:
                    vec.append(0)
    
            return vec
        
        def coworking_to_features_vec(coworking: Coworking):
            return [coworking.coordinates.lat, coworking.coordinates.lon,
                    coworking.review_count, coworking.review_rate,
                    coworking.avg_price_per_workplace]
        
        self._tags_data     = np.array(list(map(coworking_to_tags_vec, data)))
        self._features_data = np.array(list(map(coworking_to_features_vec, data)))
        
        # map coworking id to index in self._data
        self._id_to_index = { coworking.id: i for i, coworking in enumerate(data) }
        self._index_to_id = [ coworking.id for coworking in data ]

    def fit(self):
        pass

    def recommend(self, id: CoworkingId, n=4) -> List[CoworkingId]:
        # increase distance until we have at least n coworkings in the cluster
        cluster_indices = []
        d = 0
        while len(cluster_indices) < n:
            cluster_indices = self._get_cluster(id, d)
            d += 1

        cluster_features_data = self._features_data[cluster_indices]
        vec = self._features_data[self._id_to_index[id]]

        # calculate euclidean distance between vec and all other vectors in the cluster
        distances = np.power(np.subtract(vec, cluster_features_data), 2)
        distances = np.sqrt(np.sum(distances, axis=1))

        # sort distances in ascending order
        sorted_indices = np.argsort(distances)

        # the first element is the coworking itself, so remove it
        sorted_indices = sorted_indices[1:n+1]

        return [ self._index_to_id[cluster_indices[i]] for i in sorted_indices ]
    
    def _get_cluster(self, id: CoworkingId, d=3):
        vec = self._tags_data[self._id_to_index[id]]

        # calculate Manhattan distance between vec and all other vectors
        # because vec is a binary vector, Manhattan distance is the same as Hamming distance
        distances = np.abs(np.subtract(vec, self._tags_data))
        distances = np.sum(distances, axis=1)

        # get indices of all coworkings with distance <= d
        indices = np.where(distances <= d)[0]
        return indices