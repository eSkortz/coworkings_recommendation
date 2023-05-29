from abc import abstractmethod, ABCMeta
from coworking import CoworkingId
from typing import List

class Recommender(metaclass=ABCMeta):
    @abstractmethod
    def fit(self):
        raise NotImplementedError
    
    @abstractmethod
    def recommend(self, id: CoworkingId, n=4) -> List[CoworkingId]:
        raise NotImplementedError