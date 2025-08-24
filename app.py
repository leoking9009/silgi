from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import os
from werkzeug.utils import secure_filename
from config import get_config

def apply_ai_content_to_trip(trip_id, ai_content):
    """AI 생성 컨텐츠를 데이터베이스에 적용"""
    result = {'checklists': 0, 'items': 0, 'local_infos': 0, 'wishlists': 0}
    
    try:
        # 체크리스트 추가
        for checklist_data in ai_content.get('checklists', []):
            checklist = Checklist(
                trip_id=trip_id,
                category=checklist_data.get('category', '출발 전'),
                title=checklist_data.get('title', ''),
                description=checklist_data.get('description'),
                priority=checklist_data.get('priority', 'medium')
            )
            db.session.add(checklist)
            result['checklists'] += 1
        
        # 준비물품 추가
        for item_data in ai_content.get('items', []):
            item = Item(
                trip_id=trip_id,
                category=item_data.get('category', '기타'),
                name=item_data.get('name', ''),
                quantity=item_data.get('quantity', 1),
                notes=item_data.get('notes')
            )
            db.session.add(item)
            result['items'] += 1
        
        # 현지정보 추가
        for info_data in ai_content.get('local_infos', []):
            local_info = LocalInfo(
                trip_id=trip_id,
                category=info_data.get('category', '기타'),
                title=info_data.get('title', ''),
                content=info_data.get('content', ''),
                rating=info_data.get('rating'),
                phone=info_data.get('phone'),
                address=info_data.get('address')
            )
            db.session.add(local_info)
            result['local_infos'] += 1
        
        # 위시리스트 추가
        for wishlist_data in ai_content.get('wishlists', []):
            wishlist = Wishlist(
                trip_id=trip_id,
                place_name=wishlist_data.get('place_name', ''),
                category=wishlist_data.get('category', '관광지'),
                description=wishlist_data.get('description'),
                priority=wishlist_data.get('priority', 'medium'),
                address=wishlist_data.get('address')
            )
            db.session.add(wishlist)
            result['wishlists'] += 1
        
        db.session.commit()
        return result
        
    except Exception as e:
        db.session.rollback()
        raise e

app = Flask(__name__)
config_class = get_config()
app.config.from_object(config_class)

# 업로드 폴더 생성
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# 데이터베이스 모델 정의
class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 관계 정의
    checklists = db.relationship('Checklist', backref='trip', lazy=True, cascade='all, delete-orphan')
    items = db.relationship('Item', backref='trip', lazy=True, cascade='all, delete-orphan')
    local_infos = db.relationship('LocalInfo', backref='trip', lazy=True, cascade='all, delete-orphan')
    expenses = db.relationship('Expense', backref='trip', lazy=True, cascade='all, delete-orphan')
    wishlists = db.relationship('Wishlist', backref='trip', lazy=True, cascade='all, delete-orphan')
    memories = db.relationship('Memory', backref='trip', lazy=True, cascade='all, delete-orphan')

class Checklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # 출발 전, 1일차, 2일차, 3일차, 귀국 후
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    is_completed = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(20), default='medium')  # high, medium, low
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # 서류, 의류, 용품, 약품, 전자기기
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    is_packed = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class LocalInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # 환율, 긴급연락처, 교통수단, 맛집
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    address = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    website = db.Column(db.String(200))
    rating = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # 교통비, 숙박비, 식비, 쇼핑, 관광, 기타
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default='KRW')
    description = db.Column(db.String(200))
    expense_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=False)
    place_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # 관광지, 맛집, 쇼핑, 체험, 기타
    address = db.Column(db.String(200))
    description = db.Column(db.Text)
    priority = db.Column(db.String(20), default='medium')
    is_visited = db.Column(db.Boolean, default=False)
    visit_date = db.Column(db.Date)
    rating = db.Column(db.Float)
    review = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Memory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text)
    photo_path = db.Column(db.String(200))
    memory_date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 라우트 정의
@app.route('/')
def index():
    trips = Trip.query.order_by(Trip.created_at.desc()).all()
    return render_template('index.html', trips=trips)

@app.route('/trip/<int:trip_id>')
def trip_detail(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    
    # 각 카테고리별 데이터 가져오기
    checklists = Checklist.query.filter_by(trip_id=trip_id).all()
    items = Item.query.filter_by(trip_id=trip_id).all()
    local_infos = LocalInfo.query.filter_by(trip_id=trip_id).all()
    expenses = Expense.query.filter_by(trip_id=trip_id).all()
    wishlists = Wishlist.query.filter_by(trip_id=trip_id).all()
    memories = Memory.query.filter_by(trip_id=trip_id).all()
    
    # 진행률 계산
    total_checklists = len(checklists)
    completed_checklists = len([c for c in checklists if c.is_completed])
    checklist_progress = (completed_checklists / total_checklists * 100) if total_checklists > 0 else 0
    
    total_items = len(items)
    packed_items = len([i for i in items if i.is_packed])
    packing_progress = (packed_items / total_items * 100) if total_items > 0 else 0
    
    total_wishlist = len(wishlists)
    visited_places = len([w for w in wishlists if w.is_visited])
    wishlist_progress = (visited_places / total_wishlist * 100) if total_wishlist > 0 else 0
    
    return render_template('trip_detail.html', 
                         trip=trip,
                         checklists=checklists,
                         items=items,
                         local_infos=local_infos,
                         expenses=expenses,
                         wishlists=wishlists,
                         memories=memories,
                         checklist_progress=checklist_progress,
                         packing_progress=packing_progress,
                         wishlist_progress=wishlist_progress)

@app.route('/edit_trip/<int:trip_id>', methods=['GET', 'POST'])
def edit_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    
    if request.method == 'POST':
        trip.name = request.form['name']
        trip.destination = request.form['destination']
        trip.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        trip.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
        
        db.session.commit()
        flash('여행 정보가 성공적으로 수정되었습니다!', 'success')
        return redirect(url_for('trip_detail', trip_id=trip.id))
    
    return render_template('edit_trip.html', trip=trip)

@app.route('/delete_trip/<int:trip_id>', methods=['POST'])
def delete_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    
    try:
        # 관련된 모든 데이터가 CASCADE로 자동 삭제됨
        db.session.delete(trip)
        db.session.commit()
        flash(f'"{trip.name}" 여행이 완전히 삭제되었습니다.', 'success')
        return redirect(url_for('index'))
    except Exception as e:
        db.session.rollback()
        flash('여행 삭제 중 오류가 발생했습니다.', 'error')
        return redirect(url_for('trip_detail', trip_id=trip_id))

@app.route('/create_trip', methods=['GET', 'POST'])
def create_trip():
    if request.method == 'POST':
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
        days = (end_date - start_date).days + 1
        
        trip = Trip(
            name=request.form['name'],
            destination=request.form['destination'],
            start_date=start_date,
            end_date=end_date
        )
        db.session.add(trip)
        db.session.commit()
        
        # AI 기반 스마트 템플릿 적용
        use_ai = request.form.get('use_ai') == 'on'  # AI 사용 옵션
        
        try:
            if use_ai:
                # AI 기반 컨텐츠 생성
                from ai_travel_assistant import generate_ai_travel_content
                ai_content = generate_ai_travel_content(trip.destination, days, start_date)
                result = apply_ai_content_to_trip(trip.id, ai_content)
                
                flash(f'🤖 AI가 여행 계획을 생성했습니다! ✨\n'
                      f'📋 체크리스트: {result["checklists"]}개\n'
                      f'🎒 준비물품: {result["items"]}개\n'
                      f'ℹ️ 현지정보: {result["local_infos"]}개\n'
                      f'❤️ 위시리스트: {result["wishlists"]}개\n'
                      f'{trip.destination}에 특화된 AI 추천이 적용되었습니다!', 'success')
            else:
                # 기존 템플릿 방식
                from destination_templates import apply_template_to_trip
                result = apply_template_to_trip(trip.id, trip.destination, days)
                
                flash(f'여행 계획이 성공적으로 생성되었습니다! 🎉\n'
                      f'📋 체크리스트: {result["checklists"]}개\n'
                      f'🎒 준비물품: {result["items"]}개\n'
                      f'ℹ️ 현지정보: {result["local_infos"]}개\n'
                      f'❤️ 위시리스트: {result["wishlists"]}개\n'
                      f'목적지에 맞는 정보가 자동으로 추가되었습니다!', 'success')
                  
        except Exception as e:
            # 템플릿 적용 실패시 기본 체크리스트만 생성
            default_checklists = [
                {'category': '출발 전', 'title': '여권 유효기간 확인', 'priority': 'high'},
                {'category': '출발 전', 'title': '항공권 예약 확인', 'priority': 'high'},
                {'category': '출발 전', 'title': '숙소 예약 확인', 'priority': 'high'},
                {'category': '출발 전', 'title': '여행자 보험 가입', 'priority': 'medium'},
                {'category': '출발 전', 'title': '현지 화폐 환전', 'priority': 'medium'},
                {'category': '1일차', 'title': '숙소 체크인', 'priority': 'high'},
                {'category': '1일차', 'title': '현지 교통카드 구매', 'priority': 'medium'},
                {'category': '귀국 후', 'title': '사진 정리', 'priority': 'low'},
            ]
            
            for item in default_checklists:
                checklist = Checklist(
                    trip_id=trip.id,
                    category=item['category'],
                    title=item['title'],
                    priority=item['priority']
                )
                db.session.add(checklist)
            
            db.session.commit()
            flash('여행 계획이 생성되었습니다! (기본 템플릿 적용)', 'success')
        
        return redirect(url_for('trip_detail', trip_id=trip.id))
    
    return render_template('create_trip.html')

# API 엔드포인트들
@app.route('/api/toggle_checklist/<int:checklist_id>', methods=['POST'])
def toggle_checklist(checklist_id):
    checklist = Checklist.query.get_or_404(checklist_id)
    checklist.is_completed = not checklist.is_completed
    db.session.commit()
    return jsonify({'success': True, 'is_completed': checklist.is_completed})

@app.route('/api/toggle_item/<int:item_id>', methods=['POST'])
def toggle_item(item_id):
    item = Item.query.get_or_404(item_id)
    item.is_packed = not item.is_packed
    db.session.commit()
    return jsonify({'success': True, 'is_packed': item.is_packed})

@app.route('/api/toggle_wishlist/<int:wishlist_id>', methods=['POST'])
def toggle_wishlist(wishlist_id):
    wishlist = Wishlist.query.get_or_404(wishlist_id)
    wishlist.is_visited = not wishlist.is_visited
    if wishlist.is_visited:
        wishlist.visit_date = date.today()
    else:
        wishlist.visit_date = None
    db.session.commit()
    return jsonify({'success': True, 'is_visited': wishlist.is_visited})

@app.route('/api/delete_item', methods=['POST'])
def delete_item():
    try:
        item_type = request.form.get('type')
        item_id = int(request.form.get('item_id'))
        
        if item_type == 'checklist':
            item = Checklist.query.get_or_404(item_id)
        elif item_type == 'item':
            item = Item.query.get_or_404(item_id)
        elif item_type == 'localinfo':
            item = LocalInfo.query.get_or_404(item_id)
        elif item_type == 'expense':
            item = Expense.query.get_or_404(item_id)
        elif item_type == 'wishlist':
            item = Wishlist.query.get_or_404(item_id)
        elif item_type == 'memory':
            item = Memory.query.get_or_404(item_id)
        else:
            return jsonify({'success': False, 'message': '잘못된 항목 유형입니다.'})
        
        db.session.delete(item)
        db.session.commit()
        
        return jsonify({'success': True, 'message': '항목이 삭제되었습니다.'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'오류가 발생했습니다: {str(e)}'})

@app.route('/api/add_item', methods=['POST'])
def add_item():
    try:
        trip_id = request.form.get('trip_id')
        item_type = request.form.get('type')
        
        if item_type == 'checklist':
            item = Checklist(
                trip_id=trip_id,
                category=request.form.get('category'),
                title=request.form.get('title'),
                description=request.form.get('description'),
                priority=request.form.get('priority', 'medium')
            )
        elif item_type == 'item':
            item = Item(
                trip_id=trip_id,
                category=request.form.get('category'),
                name=request.form.get('name'),
                quantity=int(request.form.get('quantity', 1)),
                notes=request.form.get('notes')
            )
        elif item_type == 'localinfo':
            item = LocalInfo(
                trip_id=trip_id,
                category=request.form.get('category'),
                title=request.form.get('title'),
                content=request.form.get('content'),
                address=request.form.get('address'),
                phone=request.form.get('phone'),
                website=request.form.get('website'),
                rating=float(request.form.get('rating', 0)) if request.form.get('rating') else None
            )
        elif item_type == 'expense':
            item = Expense(
                trip_id=trip_id,
                category=request.form.get('category'),
                amount=float(request.form.get('amount')),
                currency=request.form.get('currency', 'KRW'),
                description=request.form.get('description'),
                expense_date=datetime.strptime(request.form.get('expense_date'), '%Y-%m-%d').date()
            )
        elif item_type == 'wishlist':
            item = Wishlist(
                trip_id=trip_id,
                place_name=request.form.get('place_name'),
                category=request.form.get('category'),
                address=request.form.get('address'),
                description=request.form.get('description'),
                priority=request.form.get('priority', 'medium')
            )
        elif item_type == 'memory':
            photo_path = None
            if 'photo' in request.files:
                file = request.files['photo']
                if file and file.filename != '':
                    filename = secure_filename(file.filename)
                    photo_path = filename
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            item = Memory(
                trip_id=trip_id,
                title=request.form.get('title'),
                content=request.form.get('content'),
                photo_path=photo_path,
                memory_date=datetime.strptime(request.form.get('memory_date'), '%Y-%m-%d').date(),
                location=request.form.get('location')
            )
        else:
            return jsonify({'success': False, 'message': '잘못된 항목 유형입니다.'})
        
        db.session.add(item)
        db.session.commit()
        
        return jsonify({'success': True, 'message': '항목이 추가되었습니다.'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'오류가 발생했습니다: {str(e)}'})

@app.route('/api/ai_status')
def ai_status():
    """AI 서비스 상태 확인"""
    try:
        from ai_config import AIConfig
        return jsonify({
            'available': AIConfig.is_ai_available(),
            'service': AIConfig.AI_SERVICE,
            'status': AIConfig.get_service_status()
        })
    except Exception as e:
        return jsonify({
            'available': True,  # 시뮬레이션 모드로 폴백
            'service': 'simulation',
            'status': '🤖 시뮬레이션 모드 (데모용)'
        })

@app.route('/manifest.json')
def manifest():
    return {
        "name": "여행 필수사항 관리",
        "short_name": "여행관리",
        "description": "세부 여행 필수사항을 관리하는 웹앱",
        "start_url": "/",
        "display": "standalone",
        "theme_color": "#0077be",
        "background_color": "#e8f4f8",
        "orientation": "portrait",
        "icons": [
            {
                "src": "/static/images/icon-72x72.png",
                "sizes": "72x72",
                "type": "image/png"
            },
            {
                "src": "/static/images/icon-96x96.png",
                "sizes": "96x96",
                "type": "image/png"
            },
            {
                "src": "/static/images/icon-128x128.png",
                "sizes": "128x128",
                "type": "image/png"
            },
            {
                "src": "/static/images/icon-144x144.png",
                "sizes": "144x144",
                "type": "image/png"
            },
            {
                "src": "/static/images/icon-152x152.png",
                "sizes": "152x152",
                "type": "image/png"
            },
            {
                "src": "/static/images/icon-192x192.png",
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": "/static/images/icon-384x384.png",
                "sizes": "384x384",
                "type": "image/png"
            },
            {
                "src": "/static/images/icon-512x512.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    }

# 현재 날짜를 템플릿에서 사용하기 위한 컨텍스트 프로세서
@app.context_processor
def inject_now():
    return {'today': date.today()}

# 오류 처리
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
