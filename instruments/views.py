from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Instrument
from .serializers import InstrumentSerializer

@api_view(['GET', 'POST'])
def instrument_list(request):
    if request.method == 'GET':
        instruments = Instrument.get_all()
        return Response(instruments)

    elif request.method == 'POST':
        serializer = InstrumentSerializer(data=request.data)
        if serializer.is_valid():
            new_instrument = Instrument.create(**serializer.validated_data)
            return Response(new_instrument, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def instrument_detail(request, id):
    instrument = Instrument.get_by_id(id)
    if not instrument:
        return Response({'error': 'Instrument not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(instrument)

    elif request.method == 'PUT':
        serializer = InstrumentSerializer(data=request.data)
        if serializer.is_valid():
            updated = Instrument.update(id, **serializer.validated_data)
            return Response(updated)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        Instrument.delete(id)
        return Response(status=status.HTTP_204_NO_CONTENT)
