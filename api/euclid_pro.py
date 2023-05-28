import numpy as np
from sklearn.neighbors import NearestNeighbors

def json_transformation(data):

        tags_list = ['printer', 'parking', 'restaurants', 'noize-zoning',
                    'kitchen', 'food-inside', 'board-games',
                    'rest-room', 'skype-room', 'personal-wardrobe']
        places_list = ['open_space', 'meeting_room', 'conference_room']
        review_tags_list = ['network', 'staff', 'atmosphere', 'noise-level']

        coworkings = []

        for data_counter in range(len(data)):
            # Многомерный вектор, который наполняем по параметрам
            transformed_vector = []

            # 3 параметра по типу
            if 'Коворкинг' in data[data_counter]['types']:
                transformed_vector.append(1)
            else:
                transformed_vector.append(0)
            if 'Антикафе' in data[data_counter]['types']:
                transformed_vector.append(1)
            else:
                transformed_vector.append(0)
            if 'Котокафе' in data[data_counter]['types']:
                transformed_vector.append(1)
            else:
                transformed_vector.append(0)
            
            # 2 параметра по расстоянию от центра города
            distance_from_center_lat = abs(55.558741 - data[data_counter]['coordinates']['lat'])
            distance_from_center_lon = abs(37.378847 - data[data_counter]['coordinates']['lon'])
            transformed_vector.append(distance_from_center_lat)
            transformed_vector.append(distance_from_center_lon)
            
            # 10 параметров по тегам
            for tags_counter in range(len(tags_list)):
                tag_pointer = 0
                for data_tags_counter in range(len(data[data_counter]['tags'])):
                    if data[data_counter]['tags'][data_tags_counter]['id'] == tags_list[tags_counter]:
                        tag_pointer = 1
                transformed_vector.append(tag_pointer)
            
            # 3 тега по наличию рабочих пространств
            for places_counter in range(len(places_list)):
                places_pointer = 0
                for data_places_counter in range(len(data[data_counter]['places'])):
                    if data[data_counter]['places'][data_places_counter]['type'] == places_list[places_counter]:
                        places_pointer = 1
                transformed_vector.append(places_pointer)

            # 4 тега по отзывам
            for review_tags_counter in range(len(review_tags_list)):
                review_tags_pointer = 0
                for data_review_tags_counter in range(len(data[data_counter]['review_tags'])):
                    if data[data_counter]['review_tags'][data_review_tags_counter]['type'] \
                            == review_tags_list[review_tags_counter]:
                        if data[data_counter]['review_tags'][data_review_tags_counter]['positive']:
                            review_tags_pointer += 1
                        else:
                            review_tags_pointer -= 1
                transformed_vector.append(review_tags_pointer)
            
            # 1 тег по оценке пользователей
            transformed_vector.append(data[data_counter]['review_rate'])
            
            coworking = {'id': data[data_counter]['id'], 'name': data[data_counter]['name'], 'vector': transformed_vector}
            
            coworkings.append(coworking)

        return coworkings

class EuclideanProRecommender:
    def __init__(self):
        self.coworkings = []
        self.coworking_vectors = None
        self.nearest_neighbors = None

    def add_coworking(self, coworking_id, coworking_name, vector):
        self.coworkings.append(coworking_id)
        self.coworkings.append(coworking_name)
        if self.coworking_vectors is None:
            self.coworking_vectors = np.array([vector])
        else:
            self.coworking_vectors = np.append(self.coworking_vectors, [vector], axis=0)

    def build_model(self):
        self.nearest_neighbors = NearestNeighbors(metric='euclidean')
        self.nearest_neighbors.fit(self.coworking_vectors)

    def recommend_function(self, coworking, num_recommendations=5):
        coworking_vector = np.array([coworking])
        distances, indices = self.nearest_neighbors.kneighbors(coworking_vector, n_neighbors=num_recommendations + 1)
        recommended_coworkings = [self.coworkings[i] for i in indices[0][1:]]
        return recommended_coworkings

def recommend(data, selected_coworking_id, num_recommendations=5):

    recommender = EuclideanProRecommender()

    coworkings = json_transformation(data)
    print('ok')
    for coworkings_counter in range(len(coworkings)):
        if coworkings[coworkings_counter]['id'] == selected_coworking_id:
            selected_coworking_vector = coworkings[coworkings_counter]['vector']
        recommender.add_coworking(coworkings[coworkings_counter]['id'], coworkings[coworkings_counter]['name'],
                                coworkings[coworkings_counter]['vector'])

    recommender.build_model()

    recommendations = recommender.recommend_function(selected_coworking_vector,
                                                    num_recommendations=num_recommendations)

    return recommendations