from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Weld_info, Weld_raw_data
from django.utils.timezone import now

def index(request):
    # 가장 최근의 Weld_raw_data를 가져오기
    latest_raw_data = Weld_raw_data.objects.latest('date')
    
    # 해당 model_name에 대한 Weld_info 가져오기
    try:
        weld_info = Weld_info.objects.get(model_name=latest_raw_data.model_name)
    except Weld_info.DoesNotExist:
        weld_info = None
    
    # 금일 날짜 기준으로 필터링
    today = now().date()
    today_raw_data = Weld_raw_data.objects.filter(date__date=today)
    
    # 전체 금일 생산량
    total_count = today_raw_data.count()
    
    # 금일 합격 및 불합격 갯수
    total_ok_count = today_raw_data.filter(result=True).count()
    total_ng_count = total_count - total_ok_count
    
    # 현재 모델 합격 및 불합격 갯수 (최근 모델 이름 기준)
    current_model_name = latest_raw_data.model_name
    current_model_data = today_raw_data.filter(model_name=current_model_name)
    current_model_ok_count = current_model_data.filter(result=True).count()
    current_model_ng_count = current_model_data.count() - current_model_ok_count
    
    # 조립비전 및 용접비전 결과
    before_ok_count = today_raw_data.filter(before_result=True).count()
    before_ng_count = today_raw_data.filter(before_result=False).count()
    after_ok_count = today_raw_data.filter(after_result=True).count()
    after_ng_count = today_raw_data.filter(after_result=False).count()
    total_before_count = before_ng_count + before_ok_count
    total_after_count = after_ng_count + after_ok_count

    # 템플릿에 전달할 context
    context = {
        'latest_raw_data': latest_raw_data,
        'weld_info': weld_info,
        'total_count': total_count,
        'total_ok_count': total_ok_count,
        'total_ng_count': total_ng_count,
        'current_model_ok_count': current_model_ok_count,
        'current_model_ng_count': current_model_ng_count,
        'before_ok_count': before_ok_count,
        'before_ng_count': before_ng_count,
        'after_ok_count': after_ok_count,
        'after_ng_count': after_ng_count,
        'current_time': now(),
        'total_before_count': total_before_count,
        'total_after_count': total_after_count,

    }
    
    return render(request, 'weld/main.html', context)

from django.http import JsonResponse

def get_latest_data(request):
    # 가장 최근의 Weld_raw_data를 가져오기
    latest_raw_data = Weld_raw_data.objects.latest('date')
    
    # 해당 model_name에 대한 Weld_info 가져오기
    try:
        weld_info = Weld_info.objects.get(model_name=latest_raw_data.model_name)
    except Weld_info.DoesNotExist:
        weld_info = None
    
    # 금일 날짜 기준으로 필터링
    today = now().date()
    today_raw_data = Weld_raw_data.objects.filter(date__date=today)

    # 전체 금일 생산량
    total_count = today_raw_data.count()

    # 금일 합격 및 불합격 갯수
    total_ok_count = today_raw_data.filter(result=True).count()
    total_ng_count = total_count - total_ok_count

    # 현재 모델 합격 및 불합격 갯수 (최근 모델 이름 기준)
    current_model_name = latest_raw_data.model_name
    current_model_data = today_raw_data.filter(model_name=current_model_name)
    current_model_ok_count = current_model_data.filter(result=True).count()
    current_model_ng_count = current_model_data.count() - current_model_ok_count

    # 조립비전 및 용접비전 결과
    before_ok_count = today_raw_data.filter(before_result=True).count()
    before_ng_count = today_raw_data.filter(before_result=False).count()
    after_ok_count = today_raw_data.filter(after_result=True).count()
    after_ng_count = today_raw_data.filter(after_result=False).count()
    total_before_count = before_ng_count + before_ok_count
    total_after_count = after_ng_count + after_ok_count

    data = {
        'latest_raw_data': {
            'model_id': latest_raw_data.model_id,
            'model_name': latest_raw_data.model_name,
            'result': latest_raw_data.result,
        },
        'weld_info': {
            'program': weld_info.program if weld_info else '',
            'id': weld_info.id if weld_info else '',
            'power': weld_info.power if weld_info else '',
            'freq': weld_info.freq if weld_info else '',
            'length': weld_info.length if weld_info else '',
        },
        'total_ok_count': total_ok_count,
        'total_ng_count': total_ng_count,
        'current_model_ok_count': current_model_ok_count,
        'current_model_ng_count': current_model_ng_count,
        'before_ok_count': before_ok_count,
        'before_ng_count': before_ng_count,
        'after_ok_count': after_ok_count,
        'after_ng_count': after_ng_count,
        'total_before_count': total_before_count,
        'total_after_count': total_after_count,
    }

    return JsonResponse(data)

def ping_plc(request):
    # 실제 PLC와 통신하여 상태를 확인하는 로직을 구현하세요.
    # 이 예제에서는 임의로 상태를 결정합니다.
    # 실제 구현에서는 PLC와의 연결 상태를 체크해야 합니다.

    is_connected = True  # PLC에 연결되었는지 확인하는 로직을 여기에 추가

    if is_connected:
        return JsonResponse({'status': '통신 정상'})
    else:
        return JsonResponse({'status': '통신 비정상'})

def weld_list(request):
    weld_info = Weld_info.objects.all()  # 필드명을 직접 넣고 값을 지정
    context = {'weld_info': weld_info}
    return render(request, 'weld/weld_list.html', context)

from .forms import WeldInfoForm

def weld_manage(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'register':
            form = WeldInfoForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('weld:weld_list')
        
        elif action == 'delete':
            pk = request.POST.get('id')
            weld_info = get_object_or_404(Weld_info, pk=pk)
            weld_info.delete()
            return redirect('weld:weld_list')

    else:
        form = WeldInfoForm()

    weld_info = Weld_info.objects.all()
    return render(request, 'weld/weld_manage.html', {'form': form, 'weld_info': weld_info})


from datetime import datetime
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.db.models import Case, When, IntegerField, Sum


def search_data(request):
    # GET 요청에서 날짜, 모델 이름, 그리고 검색 조건 가져오기
    start_date = request.GET.get('start_date')  # 시작 날짜
    end_date = request.GET.get('end_date')  # 종료 날짜
    query_model_name = request.GET.get('model_name')  # 모델 이름
    search_type = request.GET.get('search_type')  # 검색 조건

    # 기본적으로 모든 데이터를 조회
    raw_datas = Weld_raw_data.objects.all()

    # 날짜 범위가 주어졌을 때
    if start_date and end_date:
        if search_type == "individual" or search_type == "hourly":
            # 개별 검색 또는 시간별 검색: datetime-local 형식
            start_date = datetime.strptime(start_date, '%Y-%m-%dT%H:%M')
            end_date = datetime.strptime(end_date, '%Y-%m-%dT%H:%M')
            raw_datas = raw_datas.filter(date__range=[start_date, end_date])

        elif search_type == "daily":
            # 일별 검색: 날짜 형식 (YYYY-MM-DD)
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            raw_datas = raw_datas.filter(date__date__range=[start_date.date(), end_date.date()])

            # 일별로 OK, NG 합산 결과 계산
            raw_datas = raw_datas.values('date__date', 'model_name').annotate(
                ok_count=Count('id', filter=Q(result=True)),
                ng_count=Count('id', filter=Q(result=False)),
                total = Count('id')
            )

        elif search_type == "monthly":
            # 월별 검색: 월 형식 (YYYY-MM)
            start_date = datetime.strptime(start_date, '%Y-%m')
            end_date = datetime.strptime(end_date, '%Y-%m')
            raw_datas = raw_datas.filter(date__year__gte=start_date.year, date__year__lte=end_date.year,
                                        date__month__gte=start_date.month, date__month__lte=end_date.month)

            # 월별로 OK, NG 합산 결과 계산
            raw_datas = raw_datas.values('date__year', 'date__month', 'model_name').annotate(
                ok_count=Count('id', filter=Q(result=True)),
                ng_count=Count('id', filter=Q(result=False)),
                total = Count('id')
            )

        elif search_type == "yearly":
            # 년별 검색: 년 형식 (YYYY)
            start_date = datetime.strptime(start_date, '%Y')
            end_date = datetime.strptime(end_date, '%Y')
            raw_datas = raw_datas.filter(date__year__range=[start_date.year, end_date.year])

            # 년별로 OK, NG 합산 결과 계산
            raw_datas = raw_datas.values('date__year', 'model_name').annotate(
                ok_count=Count('id', filter=Q(result=True)),
                ng_count=Count('id', filter=Q(result=False)),
                total = Count('id')
            )

    # 모델 이름으로 필터링 (입력된 모델 이름이 있을 경우)
    if query_model_name:
        raw_datas = raw_datas.filter(model_name__icontains=query_model_name)

    # Pagination 처리
    paginator = Paginator(raw_datas, 10)  # 10개씩 페이지네이션
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'weld/search.html', {
        'page_obj': page_obj,
        'search_type': search_type,
        'start_date': start_date.strftime('%Y-%m-%dT%H:%M') if isinstance(start_date, datetime) else start_date,
        'end_date': end_date.strftime('%Y-%m-%dT%H:%M') if isinstance(end_date, datetime) else end_date,
        'model_name': query_model_name,
    })

import pandas as pd
from django.http import HttpResponse
from datetime import datetime

def download_excel(request):
    # 필터링된 데이터 가져오기
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    query_model_name = request.GET.get('model_name')
    search_type = request.GET.get('search_type')

    # 기본 데이터 쿼리 설정
    raw_datas = Weld_raw_data.objects.all()

    # 날짜 필터링
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%dT%H:%M')
        end_date = datetime.strptime(end_date, '%Y-%m-%dT%H:%M')
        raw_datas = raw_datas.filter(date__range=[start_date, end_date])

    # 모델 이름으로 필터링
    if query_model_name:
        raw_datas = raw_datas.filter(model_name__icontains=query_model_name)

    # 데이터프레임으로 변환
    data = []
    for raw_data in raw_datas:
        data.append({
            "Date": raw_data.date.replace(tzinfo=None),  # 시간대 정보 제거
            "Model Name": raw_data.model_name,
            "Result": raw_data.result,
            "Power": raw_data.power,
            "Frequency": raw_data.freq,
            "Length": raw_data.length,
        })

    df = pd.DataFrame(data)

    # 엑셀 파일로 변환
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="weld_data.xlsx"'
    with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

    return response
