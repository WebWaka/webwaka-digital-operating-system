"""
WebWaka Human Resource Management (HR) System
AI-powered HR with cultural adaptation and African workplace dynamics
"""

import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from decimal import Decimal, ROUND_HALF_UP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmployeeStatus(Enum):
    """Employee status types"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    PROBATION = "probation"
    TERMINATED = "terminated"
    SUSPENDED = "suspended"
    ON_LEAVE = "on_leave"

class LeaveType(Enum):
    """Leave types"""
    ANNUAL = "annual"
    SICK = "sick"
    MATERNITY = "maternity"
    PATERNITY = "paternity"
    COMPASSIONATE = "compassionate"
    STUDY = "study"
    UNPAID = "unpaid"
    CULTURAL_CEREMONY = "cultural_ceremony"
    PILGRIMAGE = "pilgrimage"

class PerformanceRating(Enum):
    """Performance rating levels"""
    OUTSTANDING = "outstanding"
    EXCEEDS_EXPECTATIONS = "exceeds_expectations"
    MEETS_EXPECTATIONS = "meets_expectations"
    BELOW_EXPECTATIONS = "below_expectations"
    UNSATISFACTORY = "unsatisfactory"

class TrainingStatus(Enum):
    """Training status"""
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"

@dataclass
class Employee:
    """Employee information with African cultural context"""
    employee_id: str
    tenant_id: str
    employee_number: str
    first_name: str
    last_name: str
    local_name: Optional[str]
    title: str
    department: str
    position: str
    manager_id: Optional[str]
    hire_date: datetime
    birth_date: Optional[datetime]
    gender: Optional[str]
    marital_status: Optional[str]
    phone: str
    email: Optional[str]
    address: str
    city: str
    region: str
    country: str
    nationality: str
    id_number: str
    tax_number: Optional[str]
    bank_account: Optional[str]
    emergency_contact: Dict[str, str]
    salary: Decimal
    currency: str
    employment_type: str  # full_time, part_time, contract, casual
    status: EmployeeStatus
    preferred_language: str
    cultural_background: Dict[str, Any]
    skills: List[str]
    certifications: List[str]
    education: List[Dict[str, Any]]
    work_experience: List[Dict[str, Any]]
    performance_rating: Optional[PerformanceRating]
    last_promotion: Optional[datetime]
    probation_end: Optional[datetime]
    contract_end: Optional[datetime]
    notes: str
    created_at: datetime
    updated_at: datetime

@dataclass
class LeaveRequest:
    """Leave request information"""
    request_id: str
    tenant_id: str
    employee_id: str
    leave_type: LeaveType
    start_date: datetime
    end_date: datetime
    days_requested: int
    reason: str
    status: str  # pending, approved, rejected
    approved_by: Optional[str]
    approved_at: Optional[datetime]
    rejection_reason: Optional[str]
    cultural_significance: Optional[str]
    supporting_documents: List[str]
    created_at: datetime
    updated_at: datetime

@dataclass
class PerformanceReview:
    """Performance review record"""
    review_id: str
    tenant_id: str
    employee_id: str
    reviewer_id: str
    review_period_start: datetime
    review_period_end: datetime
    overall_rating: PerformanceRating
    goals_achievement: float
    competency_scores: Dict[str, float]
    strengths: List[str]
    areas_for_improvement: List[str]
    development_plan: List[str]
    salary_recommendation: Optional[Decimal]
    promotion_recommendation: bool
    comments: str
    employee_comments: Optional[str]
    status: str  # draft, submitted, approved
    created_at: datetime
    updated_at: datetime

@dataclass
class TrainingRecord:
    """Training and development record"""
    training_id: str
    tenant_id: str
    employee_id: str
    training_name: str
    training_type: str
    provider: str
    start_date: datetime
    end_date: datetime
    duration_hours: int
    cost: Decimal
    status: TrainingStatus
    completion_score: Optional[float]
    certification_earned: Optional[str]
    skills_gained: List[str]
    feedback: Optional[str]
    created_at: datetime

class VoiceHRProcessor:
    """Process voice commands for HR operations"""
    
    def __init__(self):
        self.command_patterns = self._initialize_hr_commands()
    
    def _initialize_hr_commands(self) -> Dict[str, Dict[str, List[str]]]:
        """Initialize HR voice command patterns"""
        return {
            'en': {
                'find_employee': [
                    'find employee {name}',
                    'search for {name}',
                    'show me {name} details'
                ],
                'request_leave': [
                    'request leave for {days} days',
                    'apply for {leave_type} leave',
                    'I need {days} days off'
                ],
                'check_leave_balance': [
                    'check my leave balance',
                    'how many days do I have left',
                    'show leave balance'
                ],
                'schedule_review': [
                    'schedule review for {name}',
                    'set up performance review',
                    'plan review meeting'
                ]
            },
            'sw': {  # Swahili
                'find_employee': [
                    'tafuta mfanyakazi {name}',
                    'nionyeshe {name}'
                ],
                'request_leave': [
                    'omba likizo ya siku {days}',
                    'nataka likizo'
                ],
                'check_leave_balance': [
                    'angalia salio la likizo yangu',
                    'nina siku ngapi za likizo'
                ]
            }
        }
    
    def process_voice_command(self, command: str, language: str = 'en') -> Dict[str, Any]:
        """Process HR voice command"""
        try:
            command_lower = command.lower().strip()
            patterns = self.command_patterns.get(language, self.command_patterns['en'])
            
            for intent, pattern_list in patterns.items():
                for pattern in pattern_list:
                    match_result = self._match_hr_pattern(command_lower, pattern)
                    if match_result:
                        return {
                            'intent': intent,
                            'entities': match_result,
                            'original_command': command,
                            'language': language,
                            'confidence': 0.9
                        }
            
            return self._ai_powered_hr_nlu(command, language)
            
        except Exception as e:
            logger.error(f"HR voice command processing failed: {str(e)}")
            return {
                'intent': 'unknown',
                'entities': {},
                'error': str(e)
            }
    
    def _match_hr_pattern(self, command: str, pattern: str) -> Optional[Dict[str, str]]:
        """Match HR command pattern"""
        import re
        
        regex_pattern = pattern.replace('{name}', r'([a-zA-Z\s]+)')
        regex_pattern = regex_pattern.replace('{days}', r'(\d+)')
        regex_pattern = regex_pattern.replace('{leave_type}', r'(annual|sick|maternity|paternity)')
        
        match = re.search(regex_pattern, command, re.IGNORECASE)
        
        if match:
            entities = {}
            groups = match.groups()
            
            if '{name}' in pattern and len(groups) > 0:
                entities['name'] = groups[0].strip()
            if '{days}' in pattern:
                for group in groups:
                    if group.isdigit():
                        entities['days'] = int(group)
                        break
            if '{leave_type}' in pattern:
                for group in groups:
                    if group.lower() in ['annual', 'sick', 'maternity', 'paternity']:
                        entities['leave_type'] = group.lower()
                        break
            
            return entities
        
        return None
    
    def _ai_powered_hr_nlu(self, command: str, language: str) -> Dict[str, Any]:
        """AI-powered HR natural language understanding"""
        return {
            'intent': 'unknown',
            'entities': {},
            'original_command': command,
            'language': language,
            'confidence': 0.3,
            'ai_processed': True
        }

class HRAnalytics:
    """HR analytics and workforce insights"""
    
    def __init__(self):
        self.turnover_indicators = [
            'low_performance_rating',
            'no_recent_promotion',
            'high_absence_rate',
            'low_training_participation',
            'manager_relationship_issues'
        ]
    
    def calculate_employee_satisfaction_score(self, employee: Employee,
                                            performance_reviews: List[PerformanceReview],
                                            leave_requests: List[LeaveRequest],
                                            training_records: List[TrainingRecord]) -> float:
        """Calculate employee satisfaction score"""
        try:
            score = 5.0  # Base score
            
            # Performance trend
            if performance_reviews:
                recent_reviews = sorted(performance_reviews, key=lambda x: x.created_at, reverse=True)[:3]
                avg_rating = self._rating_to_score(recent_reviews[0].overall_rating)
                score += (avg_rating - 3) * 0.5  # Adjust based on performance
            
            # Leave utilization (healthy work-life balance indicator)
            annual_leaves = [lr for lr in leave_requests if lr.leave_type == LeaveType.ANNUAL]
            if len(annual_leaves) > 0:
                score += 0.3  # Taking leave is positive
            elif len(annual_leaves) == 0 and len(leave_requests) > 5:
                score -= 0.2  # Too many sick leaves might indicate issues
            
            # Training and development
            recent_training = [tr for tr in training_records if tr.created_at > datetime.utcnow() - timedelta(days=365)]
            if len(recent_training) > 2:
                score += 0.4  # Good development opportunities
            elif len(recent_training) == 0:
                score -= 0.3  # Lack of development
            
            # Tenure consideration
            tenure_years = (datetime.utcnow() - employee.hire_date).days / 365
            if tenure_years > 2:
                score += 0.2  # Stability bonus
            
            return max(1.0, min(5.0, score))
            
        except Exception as e:
            logger.error(f"Satisfaction score calculation failed: {str(e)}")
            return 3.0  # Default neutral score
    
    def _rating_to_score(self, rating: PerformanceRating) -> float:
        """Convert performance rating to numeric score"""
        rating_map = {
            PerformanceRating.OUTSTANDING: 5.0,
            PerformanceRating.EXCEEDS_EXPECTATIONS: 4.0,
            PerformanceRating.MEETS_EXPECTATIONS: 3.0,
            PerformanceRating.BELOW_EXPECTATIONS: 2.0,
            PerformanceRating.UNSATISFACTORY: 1.0
        }
        return rating_map.get(rating, 3.0)
    
    def predict_turnover_risk(self, employee: Employee,
                             performance_reviews: List[PerformanceReview],
                             leave_requests: List[LeaveRequest],
                             training_records: List[TrainingRecord]) -> Dict[str, Any]:
        """Predict employee turnover risk"""
        try:
            risk_score = 0.0
            risk_factors = []
            
            # Performance trend
            if performance_reviews:
                recent_review = max(performance_reviews, key=lambda x: x.created_at)
                if recent_review.overall_rating in [PerformanceRating.BELOW_EXPECTATIONS, PerformanceRating.UNSATISFACTORY]:
                    risk_score += 0.3
                    risk_factors.append('poor_performance')
            
            # Promotion stagnation
            if employee.last_promotion:
                months_since_promotion = (datetime.utcnow() - employee.last_promotion).days / 30
                if months_since_promotion > 24:  # No promotion in 2 years
                    risk_score += 0.2
                    risk_factors.append('promotion_stagnation')
            else:
                # Never promoted
                tenure_months = (datetime.utcnow() - employee.hire_date).days / 30
                if tenure_months > 18:
                    risk_score += 0.25
                    risk_factors.append('no_career_progression')
            
            # Training participation
            recent_training = [tr for tr in training_records if tr.created_at > datetime.utcnow() - timedelta(days=365)]
            if len(recent_training) == 0:
                risk_score += 0.15
                risk_factors.append('no_development_opportunities')
            
            # Leave patterns
            sick_leaves = [lr for lr in leave_requests if lr.leave_type == LeaveType.SICK]
            if len(sick_leaves) > 8:  # Excessive sick leave
                risk_score += 0.1
                risk_factors.append('high_absenteeism')
            
            # Salary stagnation (if no recent salary increase)
            # This would require salary history data
            
            # Determine risk level
            if risk_score >= 0.6:
                risk_level = 'high'
            elif risk_score >= 0.3:
                risk_level = 'medium'
            else:
                risk_level = 'low'
            
            return {
                'employee_id': employee.employee_id,
                'risk_score': min(risk_score, 1.0),
                'risk_level': risk_level,
                'risk_factors': risk_factors,
                'recommendations': self._generate_retention_recommendations(risk_factors)
            }
            
        except Exception as e:
            logger.error(f"Turnover prediction failed: {str(e)}")
            return {
                'employee_id': employee.employee_id,
                'risk_score': 0.0,
                'risk_level': 'unknown',
                'error': str(e)
            }
    
    def _generate_retention_recommendations(self, risk_factors: List[str]) -> List[str]:
        """Generate employee retention recommendations"""
        recommendations = []
        
        if 'poor_performance' in risk_factors:
            recommendations.append('Implement performance improvement plan')
            recommendations.append('Provide additional training and support')
        
        if 'promotion_stagnation' in risk_factors or 'no_career_progression' in risk_factors:
            recommendations.append('Discuss career development opportunities')
            recommendations.append('Consider promotion or role expansion')
        
        if 'no_development_opportunities' in risk_factors:
            recommendations.append('Enroll in relevant training programs')
            recommendations.append('Assign mentorship or coaching')
        
        if 'high_absenteeism' in risk_factors:
            recommendations.append('Investigate underlying health or personal issues')
            recommendations.append('Consider flexible work arrangements')
        
        return recommendations

class HRManager:
    """Main HR management system"""
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.employees = {}
        self.leave_requests = {}
        self.performance_reviews = {}
        self.training_records = {}
        self.voice_processor = VoiceHRProcessor()
        self.analytics = HRAnalytics()
        self.cultural_adapter = AfricanHRAdapter()
    
    def add_employee(self, employee_data: Dict[str, Any]) -> Employee:
        """Add new employee"""
        try:
            employee_id = str(uuid.uuid4())
            employee_number = employee_data.get('employee_number', f"EMP-{employee_id[:8]}")
            
            employee = Employee(
                employee_id=employee_id,
                tenant_id=self.tenant_id,
                employee_number=employee_number,
                first_name=employee_data['first_name'],
                last_name=employee_data['last_name'],
                local_name=employee_data.get('local_name'),
                title=employee_data['title'],
                department=employee_data['department'],
                position=employee_data['position'],
                manager_id=employee_data.get('manager_id'),
                hire_date=employee_data.get('hire_date', datetime.utcnow()),
                birth_date=employee_data.get('birth_date'),
                gender=employee_data.get('gender'),
                marital_status=employee_data.get('marital_status'),
                phone=employee_data['phone'],
                email=employee_data.get('email'),
                address=employee_data.get('address', ''),
                city=employee_data.get('city', ''),
                region=employee_data.get('region', ''),
                country=employee_data.get('country', ''),
                nationality=employee_data.get('nationality', ''),
                id_number=employee_data['id_number'],
                tax_number=employee_data.get('tax_number'),
                bank_account=employee_data.get('bank_account'),
                emergency_contact=employee_data.get('emergency_contact', {}),
                salary=Decimal(str(employee_data.get('salary', 0))),
                currency=employee_data.get('currency', 'USD'),
                employment_type=employee_data.get('employment_type', 'full_time'),
                status=EmployeeStatus(employee_data.get('status', 'probation')),
                preferred_language=employee_data.get('preferred_language', 'en'),
                cultural_background=employee_data.get('cultural_background', {}),
                skills=employee_data.get('skills', []),
                certifications=employee_data.get('certifications', []),
                education=employee_data.get('education', []),
                work_experience=employee_data.get('work_experience', []),
                performance_rating=None,
                last_promotion=employee_data.get('last_promotion'),
                probation_end=employee_data.get('probation_end'),
                contract_end=employee_data.get('contract_end'),
                notes=employee_data.get('notes', ''),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            self.employees[employee_id] = employee
            
            # Apply cultural adaptations
            self.cultural_adapter.adapt_employee_profile(employee)
            
            logger.info(f"Added employee {employee.first_name} {employee.last_name} with ID {employee_id}")
            return employee
            
        except Exception as e:
            logger.error(f"Employee addition failed: {str(e)}")
            raise HRException(f"Employee addition failed: {str(e)}")
    
    def submit_leave_request(self, request_data: Dict[str, Any]) -> LeaveRequest:
        """Submit leave request"""
        try:
            request_id = str(uuid.uuid4())
            
            start_date = request_data['start_date']
            end_date = request_data['end_date']
            days_requested = (end_date - start_date).days + 1
            
            leave_request = LeaveRequest(
                request_id=request_id,
                tenant_id=self.tenant_id,
                employee_id=request_data['employee_id'],
                leave_type=LeaveType(request_data['leave_type']),
                start_date=start_date,
                end_date=end_date,
                days_requested=days_requested,
                reason=request_data.get('reason', ''),
                status='pending',
                approved_by=None,
                approved_at=None,
                rejection_reason=None,
                cultural_significance=request_data.get('cultural_significance'),
                supporting_documents=request_data.get('supporting_documents', []),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            self.leave_requests[request_id] = leave_request
            
            # Apply cultural considerations
            self.cultural_adapter.adapt_leave_request(leave_request)
            
            logger.info(f"Submitted leave request {request_id} for employee {request_data['employee_id']}")
            return leave_request
            
        except Exception as e:
            logger.error(f"Leave request submission failed: {str(e)}")
            raise HRException(f"Leave request submission failed: {str(e)}")
    
    def process_voice_command(self, command: str, language: str = 'en',
                             employee_id: str = None) -> Dict[str, Any]:
        """Process voice command for HR operations"""
        try:
            command_result = self.voice_processor.process_voice_command(command, language)
            
            if command_result['confidence'] < 0.5:
                return {
                    'success': False,
                    'message': 'Could not understand the HR command',
                    'original_command': command
                }
            
            intent = command_result['intent']
            entities = command_result['entities']
            
            if intent == 'find_employee':
                return self._handle_find_employee_voice(entities, command)
            elif intent == 'request_leave':
                return self._handle_request_leave_voice(entities, command, employee_id)
            elif intent == 'check_leave_balance':
                return self._handle_check_leave_balance_voice(entities, command, employee_id)
            else:
                return {
                    'success': False,
                    'message': f'Unknown HR command: {intent}',
                    'original_command': command
                }
                
        except Exception as e:
            logger.error(f"HR voice command processing failed: {str(e)}")
            return {
                'success': False,
                'message': 'HR voice command processing failed',
                'error': str(e)
            }
    
    def _handle_find_employee_voice(self, entities: Dict[str, Any], 
                                   original_command: str) -> Dict[str, Any]:
        """Handle find employee voice command"""
        try:
            name = entities.get('name', '').strip()
            if not name:
                return {
                    'success': False,
                    'message': 'Employee name not specified',
                    'original_command': original_command
                }
            
            # Search employees by name
            matching_employees = []
            name_lower = name.lower()
            
            for employee in self.employees.values():
                full_name = f"{employee.first_name} {employee.last_name}".lower()
                if (name_lower in full_name or 
                    (employee.local_name and name_lower in employee.local_name.lower()) or
                    name_lower in employee.employee_number.lower()):
                    matching_employees.append(employee)
            
            if not matching_employees:
                return {
                    'success': False,
                    'message': f'No employees found matching "{name}"',
                    'original_command': original_command
                }
            
            return {
                'success': True,
                'message': f'Found {len(matching_employees)} employee(s)',
                'employees': [
                    {
                        'employee_id': e.employee_id,
                        'name': f"{e.first_name} {e.last_name}",
                        'employee_number': e.employee_number,
                        'department': e.department,
                        'position': e.position,
                        'status': e.status.value
                    }
                    for e in matching_employees
                ],
                'original_command': original_command
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': 'Employee search failed',
                'error': str(e)
            }
    
    def create_performance_review(self, review_data: Dict[str, Any]) -> PerformanceReview:
        """Create performance review"""
        try:
            review_id = str(uuid.uuid4())
            
            review = PerformanceReview(
                review_id=review_id,
                tenant_id=self.tenant_id,
                employee_id=review_data['employee_id'],
                reviewer_id=review_data['reviewer_id'],
                review_period_start=review_data['review_period_start'],
                review_period_end=review_data['review_period_end'],
                overall_rating=PerformanceRating(review_data['overall_rating']),
                goals_achievement=review_data.get('goals_achievement', 0.0),
                competency_scores=review_data.get('competency_scores', {}),
                strengths=review_data.get('strengths', []),
                areas_for_improvement=review_data.get('areas_for_improvement', []),
                development_plan=review_data.get('development_plan', []),
                salary_recommendation=Decimal(str(review_data['salary_recommendation'])) if review_data.get('salary_recommendation') else None,
                promotion_recommendation=review_data.get('promotion_recommendation', False),
                comments=review_data.get('comments', ''),
                employee_comments=review_data.get('employee_comments'),
                status='draft',
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            self.performance_reviews[review_id] = review
            
            logger.info(f"Created performance review {review_id} for employee {review_data['employee_id']}")
            return review
            
        except Exception as e:
            logger.error(f"Performance review creation failed: {str(e)}")
            raise HRException(f"Performance review creation failed: {str(e)}")
    
    def get_employee_analytics(self, employee_id: str) -> Dict[str, Any]:
        """Get comprehensive employee analytics"""
        try:
            employee = self.employees.get(employee_id)
            if not employee:
                raise HRException(f"Employee {employee_id} not found")
            
            # Get employee data
            employee_reviews = [r for r in self.performance_reviews.values() if r.employee_id == employee_id]
            employee_leaves = [l for l in self.leave_requests.values() if l.employee_id == employee_id]
            employee_training = [t for t in self.training_records.values() if t.employee_id == employee_id]
            
            # Calculate satisfaction score
            satisfaction_score = self.analytics.calculate_employee_satisfaction_score(
                employee, employee_reviews, employee_leaves, employee_training
            )
            
            # Predict turnover risk
            turnover_risk = self.analytics.predict_turnover_risk(
                employee, employee_reviews, employee_leaves, employee_training
            )
            
            # Calculate tenure
            tenure_days = (datetime.utcnow() - employee.hire_date).days
            
            return {
                'employee': {
                    'employee_id': employee.employee_id,
                    'name': f"{employee.first_name} {employee.last_name}",
                    'department': employee.department,
                    'position': employee.position,
                    'status': employee.status.value,
                    'tenure_days': tenure_days
                },
                'satisfaction_score': satisfaction_score,
                'turnover_risk': turnover_risk,
                'performance_reviews_count': len(employee_reviews),
                'leave_requests_count': len(employee_leaves),
                'training_completed': len([t for t in employee_training if t.status == TrainingStatus.COMPLETED])
            }
            
        except Exception as e:
            logger.error(f"Employee analytics failed: {str(e)}")
            raise HRException(f"Employee analytics failed: {str(e)}")
    
    def get_hr_dashboard(self) -> Dict[str, Any]:
        """Get HR dashboard data"""
        try:
            total_employees = len(self.employees)
            active_employees = len([e for e in self.employees.values() if e.status == EmployeeStatus.ACTIVE])
            pending_leaves = len([l for l in self.leave_requests.values() if l.status == 'pending'])
            
            # Department breakdown
            dept_breakdown = {}
            for employee in self.employees.values():
                dept = employee.department
                dept_breakdown[dept] = dept_breakdown.get(dept, 0) + 1
            
            # Recent hires (last 30 days)
            recent_hires = [
                e for e in self.employees.values() 
                if e.hire_date > datetime.utcnow() - timedelta(days=30)
            ]
            
            return {
                'summary': {
                    'total_employees': total_employees,
                    'active_employees': active_employees,
                    'pending_leave_requests': pending_leaves,
                    'recent_hires': len(recent_hires)
                },
                'department_breakdown': dept_breakdown,
                'recent_hires': [
                    {
                        'employee_id': e.employee_id,
                        'name': f"{e.first_name} {e.last_name}",
                        'department': e.department,
                        'hire_date': e.hire_date.isoformat()
                    }
                    for e in recent_hires
                ]
            }
            
        except Exception as e:
            logger.error(f"HR dashboard generation failed: {str(e)}")
            raise HRException(f"HR dashboard generation failed: {str(e)}")

class AfricanHRAdapter:
    """Adapt HR for African cultural contexts"""
    
    def __init__(self):
        self.cultural_leave_types = {
            'cultural_ceremony': {
                'description': 'Traditional ceremonies and cultural events',
                'typical_duration': 3,
                'requires_documentation': False
            },
            'pilgrimage': {
                'description': 'Religious pilgrimage (Hajj, etc.)',
                'typical_duration': 14,
                'requires_documentation': True
            },
            'extended_family_support': {
                'description': 'Supporting extended family members',
                'typical_duration': 5,
                'requires_documentation': False
            }
        }
    
    def adapt_employee_profile(self, employee: Employee):
        """Adapt employee profile for African context"""
        if not employee.cultural_background:
            employee.cultural_background = {}
        
        # Add African-specific cultural considerations
        employee.cultural_background.setdefault('extended_family_obligations', True)
        employee.cultural_background.setdefault('community_responsibilities', True)
        employee.cultural_background.setdefault('traditional_ceremonies', True)
        
        # Language considerations
        if employee.preferred_language != 'en':
            employee.cultural_background['requires_translation_support'] = True
    
    def adapt_leave_request(self, leave_request: LeaveRequest):
        """Adapt leave request for African cultural context"""
        # Cultural ceremony leave gets automatic consideration
        if leave_request.leave_type == LeaveType.CULTURAL_CEREMONY:
            leave_request.cultural_significance = "Traditional cultural ceremony - important for community standing"
        
        # Extended approval for pilgrimage
        if leave_request.leave_type == LeaveType.PILGRIMAGE:
            leave_request.cultural_significance = "Religious obligation - requires extended leave period"

class HRException(Exception):
    """Custom HR exception"""
    pass

# Example usage and testing
def create_sample_hr_system():
    """Create sample HR system for testing"""
    hr = HRManager("tenant_123")
    
    # Add sample employees
    employees_data = [
        {
            'first_name': 'Fatima',
            'last_name': 'Kone',
            'local_name': 'Mama Fatima',
            'title': 'Ms.',
            'department': 'Sales',
            'position': 'Sales Manager',
            'phone': '+223123456789',
            'email': 'fatima@example.com',
            'id_number': 'ML123456789',
            'salary': 50000,
            'currency': 'XOF',
            'country': 'Mali',
            'preferred_language': 'fr'
        },
        {
            'first_name': 'Kofi',
            'last_name': 'Mensah',
            'title': 'Mr.',
            'department': 'IT',
            'position': 'Software Developer',
            'phone': '+233241234567',
            'email': 'kofi@example.com',
            'id_number': 'GH987654321',
            'salary': 30000,
            'currency': 'GHS',
            'country': 'Ghana',
            'preferred_language': 'en'
        }
    ]
    
    for employee_data in employees_data:
        hr.add_employee(employee_data)
    
    return hr

# Initialize HR system
hr_system = create_sample_hr_system()

