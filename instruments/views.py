from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from django.conf import settings
import os

@csrf_exempt
@require_http_methods(["GET", "POST"])
def instrument_list(request):
    json_file = os.path.join(settings.BASE_DIR, 'instruments_data.json')
    
    # Garante que o arquivo existe e é válido
    if not os.path.exists(json_file):
        with open(json_file, 'w') as f:
            json.dump([], f)
    
    if request.method == 'GET':
        try:
            with open(json_file, 'r') as f:
                instruments = json.load(f)
                if not isinstance(instruments, list):
                    raise ValueError("Formato inválido do arquivo JSON")
            return JsonResponse(instruments, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == 'POST':
        try:
            # Verifica o tipo de conteúdo
            if request.content_type != 'application/json':
                return JsonResponse({'error': 'Content-Type deve ser application/json'}, status=400)
            
            # Carrega os dados do corpo da requisição
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'JSON inválido'}, status=400)
            
            # Validação dos campos obrigatórios
            required_fields = ['name', 'category', 'price']
            for field in required_fields:
                if field not in data or not str(data[field]).strip():
                    return JsonResponse({'error': f'Campo {field} é obrigatório'}, status=400)
            
            # Converte o preço
            try:
                price = float(data['price'])
            except (ValueError, TypeError):
                return JsonResponse({'error': 'Preço deve ser um número válido'}, status=400)
            
            # Processa o cadastro
            with open(json_file, 'r+') as f:
                try:
                    instruments = json.load(f)
                    if not isinstance(instruments, list):
                        instruments = []
                except json.JSONDecodeError:
                    instruments = []
                
                new_id = max([i.get('id', 0) for i in instruments], default=0) + 1
                new_instrument = {
                    'id': new_id,
                    'name': str(data['name']).strip(),
                    'category': str(data['category']).strip(),
                    'price': price,
                    'description': str(data.get('description', '')).strip()
                }
                
                instruments.append(new_instrument)
                f.seek(0)
                json.dump(instruments, f, indent=4)
                f.truncate()
            
            return JsonResponse(new_instrument, status=201)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def instrument_detail(request, id):
    json_file = os.path.join(settings.BASE_DIR, 'instruments_data.json')
    
    try:
        with open(json_file, 'r') as f:
            instruments = json.load(f)
            if not isinstance(instruments, list):
                instruments = []
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    try:
        instrument_id = int(id)
    except ValueError:
        return JsonResponse({'error': 'ID inválido'}, status=400)

    instrument = next((i for i in instruments if i.get('id') == instrument_id), None)
    if not instrument:
        return JsonResponse({'error': 'Instrumento não encontrado'}, status=404)

    if request.method == 'GET':
        return JsonResponse(instrument)

    elif request.method == 'PUT':
        try:
            if request.content_type != 'application/json':
                return JsonResponse({'error': 'Content-Type deve ser application/json'}, status=400)
            
            data = json.loads(request.body)
            
            # Atualiza apenas os campos fornecidos
            updated_fields = {}
            if 'name' in data:
                updated_fields['name'] = str(data['name']).strip()
            if 'category' in data:
                updated_fields['category'] = str(data['category']).strip()
            if 'price' in data:
                try:
                    updated_fields['price'] = float(data['price'])
                except (ValueError, TypeError):
                    return JsonResponse({'error': 'Preço deve ser um número válido'}, status=400)
            if 'description' in data:
                updated_fields['description'] = str(data['description']).strip()
            
            # Aplica as atualizações
            for i, item in enumerate(instruments):
                if item.get('id') == instrument_id:
                    instruments[i].update(updated_fields)
                    with open(json_file, 'w') as f:
                        json.dump(instruments, f, indent=4)
                    return JsonResponse(instruments[i])
            
            return JsonResponse({'error': 'Instrumento não encontrado'}, status=404)
                    
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == 'DELETE':
        try:
            new_instruments = [i for i in instruments if i.get('id') != instrument_id]
            if len(new_instruments) == len(instruments):
                return JsonResponse({'error': 'Instrumento não encontrado'}, status=404)
            
            with open(json_file, 'w') as f:
                json.dump(new_instruments, f, indent=4)
            return JsonResponse({'success': True}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)