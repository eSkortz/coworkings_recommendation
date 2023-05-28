from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from drf_yasg import openapi

from . import euclid, euclid_pro, cluster, hamming
from .coworking import Coworking
import json

class MyView(viewsets.ViewSet):

    # Подборка на основе евклида
    @csrf_exempt
    @swagger_auto_schema(
        method='post',
        tags=['Подборка по евклиду'],
        operation_id = 'Функция для составления списка рекомендаций по евклиду',
        operation_description = 'Эта функция используется чтобы сделать выборку по коворкингам по стандартной евклидовой метрике',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['coworking_id', 'num_recommendations'],
            properties={
                'coworking_id': openapi.Schema(type=openapi.TYPE_STRING),
                'num_recommendations': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            200: openapi.Response(
                description='Успешное получение списка рекомендаций',
                examples={
                    'application/json': {
                        'success': '[recommendations_list]'
                    }
                }
            ),
            400: openapi.Response(
                description='Некорректные данные запроса',
                examples={
                    'application/json': {
                        'error': 'Что-то пошло не так'
                    }
                }
            ),
            405: openapi.Response(
                description='Метод не разрешен',
                examples={
                    'application/json': {
                        'error': 'Неверный метод запроса'
                    }
                }
            ),
        }
    )
    @api_view(['POST'])
    def euclid(request):
        if request.method == 'POST':
            coworking_id = request.POST.get('coworking_id')
            num_recommendations = request.POST.get('num_recommendations')
            with open('coworkings.json', 'r') as file:
                json_data = json.load(file)
            data = Coworking.schema().load(json_data, many=True)
            try:
                algo = euclid.EuclideanRecommender(data)
                algo.fit()
                recommendations = algo.recommend(int(coworking_id), int(num_recommendations))
                print(recommendations)
            except Exception:
                return Response(data={'error':'sth went wrong'}, status = 400)
            else:
                coworking_list = []
                for reccomendations_counter in range(len(recommendations)):
                    for coworkings_counter in range(len(json_data)):
                        if json_data[coworkings_counter]['id'] == recommendations[reccomendations_counter]:
                            coworking_list.append(json_data[coworkings_counter])
                return Response(data={'success':coworking_list}, status=200)
        else:
            return Response(data={'error': 'Неверный метод запроса'}, status=405)


    # Подборка по кластеризации
    @csrf_exempt
    @swagger_auto_schema(
        method='post',
        tags=['Подборка по кластеризации'],
        operation_id = 'Функция для составления списка рекомендаций по кластеризации',
        operation_description = 'Эта функция используется чтобы сделать выборку по коворкингам по принципу кластеризации',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['coworking_id', 'num_recommendations'],
            properties={
                'coworking_id': openapi.Schema(type=openapi.TYPE_STRING),
                'num_recommendations': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            200: openapi.Response(
                description='Успешное получение списка рекомендаций',
                examples={
                    'application/json': {
                        'success': '[recommendations_list]'
                    }
                }
            ),
            400: openapi.Response(
                description='Некорректные данные запроса',
                examples={
                    'application/json': {
                        'error': 'Что-то пошло не так'
                    }
                }
            ),
            405: openapi.Response(
                description='Метод не разрешен',
                examples={
                    'application/json': {
                        'error': 'Неверный метод запроса'
                    }
                }
            ),
        }
    )
    @api_view(['POST'])
    def cluster(request):
        if request.method == 'POST':
            coworking_id = request.POST.get('coworking_id')
            num_recommendations = request.POST.get('num_recommendations')
            with open('coworkings.json', 'r') as file:
                json_data = json.load(file)
            data = Coworking.schema().load(json_data, many=True)
            try:
                algo = cluster.ClusteringRecommender(data)
                algo.fit()
                recommendations = algo.recommend(int(coworking_id), int(num_recommendations))
            except Exception:
                return Response(data={'error':'sth went wrong'}, status = 400)
            else:
                coworking_list = []
                for recommendations_counter in range(len(recommendations)):
                    for coworkings_counter in range(len(json_data)):
                        if json_data[coworkings_counter]['id'] == recommendations[recommendations_counter]:
                            coworking_list.append(json_data[coworkings_counter])
                return Response(data={'success':coworking_list}, status=200)
        else:
            return Response(data={'error': 'Неверный метод запроса'}, status=405)


    # Подборка по гаммингу
    @csrf_exempt
    @swagger_auto_schema(
        method='post',
        tags=['Подборка по гаммингу'],
        operation_id = 'Функция для составления списка рекомендаций по гаммингу',
        operation_description = 'Эта функция используется чтобы сделать выборку по коворкингам по принципу гамминга',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['coworking_id', 'num_recommendations'],
            properties={
                'coworking_id': openapi.Schema(type=openapi.TYPE_STRING),
                'num_recommendations': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            200: openapi.Response(
                description='Успешное получение списка рекомендаций',
                examples={
                    'application/json': {
                        'success': '[recommendations_list]'
                    }
                }
            ),
            400: openapi.Response(
                description='Некорректные данные запроса',
                examples={
                    'application/json': {
                        'error': 'Что-то пошло не так'
                    }
                }
            ),
            405: openapi.Response(
                description='Метод не разрешен',
                examples={
                    'application/json': {
                        'error': 'Неверный метод запроса'
                    }
                }
            ),
        }
    )
    @api_view(['POST'])
    def hamming(request):
        if request.method == 'POST':
            coworking_id = request.POST.get('coworking_id')
            num_recommendations = request.POST.get('num_recommendations')
            with open('coworkings.json', 'r') as file:
                json_data = json.load(file)
            data = Coworking.schema().load(json_data, many=True)
            try:
                algo = hamming.HammingRecommender(data)
                algo.fit()
                recommendations = algo.recommend(int(coworking_id), int(num_recommendations))
            except Exception:
                return Response(data={'error':'sth went wrong'}, status = 400)
            else:
                coworking_list = []
                for reccomendations_counter in range(len(recommendations)):
                    for coworkings_counter in range(len(json_data)):
                        if json_data[coworkings_counter]['id'] == recommendations[reccomendations_counter]:
                            coworking_list.append(json_data[coworkings_counter])
                return Response(data={'success':coworking_list}, status=200)
        else:
            return Response(data={'error': 'Неверный метод запроса'}, status=405)


    # Ппрлдвинутая подборка по евклиду
    @csrf_exempt
    @swagger_auto_schema(
        method='post',
        tags=['Подборка по евклиду с большей точностью'],
        operation_id = 'Функция для составления списка рекомендаций по евклиду с лучшей точностью',
        operation_description = 'Эта функция используется чтобы сделать выборку по коворкингам по евклюдовой метрике с наибольшей точностью',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['coworking_id', 'num_recommendations'],
            properties={
                'coworking_id': openapi.Schema(type=openapi.TYPE_STRING),
                'num_recommendations': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            200: openapi.Response(
                description='Успешное получение списка рекомендаций',
                examples={
                    'application/json': {
                        'success': '[recommendations_list]'
                    }
                }
            ),
            400: openapi.Response(
                description='Некорректные данные запроса',
                examples={
                    'application/json': {
                        'error': 'Что-то пошло не так'
                    }
                }
            ),
            405: openapi.Response(
                description='Метод не разрешен',
                examples={
                    'application/json': {
                        'error': 'Неверный метод запроса'
                    }
                }
            ),
        }
    )
    @api_view(['POST'])
    def euclid_pro(request):
        if request.method == 'POST':
            coworking_id = request.POST.get('coworking_id')
            num_recommendations = request.POST.get('num_recommendations')
            with open('coworkings.json', 'r') as file:
                json_data = json.load(file)
            try:
                recommendations = euclid_pro.recommend(json_data, int(coworking_id), int(num_recommendations))
            except Exception:
                return Response(data={'error':'sth went wrong'}, status = 400)
            else:
                coworking_list = []
                for reccomendations_counter in range(len(recommendations)):
                    for coworkings_counter in range(len(json_data)):
                        if json_data[coworkings_counter]['id'] == recommendations[reccomendations_counter]:
                            coworking_list.append(json_data[coworkings_counter])
                return Response(data={'success':coworking_list}, status=200)
        else:
            return Response(data={'error': 'Неверный метод запроса'}, status=405)
