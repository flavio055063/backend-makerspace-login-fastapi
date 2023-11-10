from sqlalchemy import Column, String, Integer, Float, Boolean, Date, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base

class CustomerModel(Base):
    __tablename__ = 'customer'
    customer_id = Column('customer_id', Integer, primary_key=True, nullable=False, autoincrement=True)
    customer_name = Column('customer_name', String, nullable=False)
    cpf = Column('cpf', String, nullable=False, unique=True)
    rua  = Column('rua', String, nullable=False)
    bairro = Column('bairro', String, nullable=False)
    cidade = Column('cidade', String, nullable=False)
    estado = Column('estado', String, nullable=False)
    cep = Column('cep', String, nullable=False)
    email = Column('email', String, nullable=False, unique=True, index=True)
    password_hash = Column('password_hash', String, nullable=False)

class BudgetModel(Base):
    __tablename__ = "budget"
    budget_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customer.customer_id"))
    serviceDescription = Column(String)
    category = Column(String) #values must be in: [3dprint, lasercut, cnc, other]
    price = Column(Float)
    isApproved = Column(Boolean)
    paymentStatus = Column(String) #values must be: inAnalysis, notPaid or paid
    status = Column(String) #values must be: [inAnalysis, awaitingForAproval, notApproved, approved, toDo, inProgress, Done, Delivered]
    budget_solicitated_date = Column(DateTime)
    service_payment_date = Column(Date)
    service_start_date = Column(Date)
    service_end_date = Column(Date)
    delivery_date = Column(Date)
    customer = relationship("CustomerModel")

class ConsumesModel(Base):
    __tablename__ = "consumes"
    budget_id = Column(Integer, ForeignKey("budget.budget_id"))
    material_id = Column(Integer, ForeignKey("materials.material_id"))
    quantity = Column(Integer, nullable=False)
    budget = relationship("BudgetModel")
    material = relationship("MaterialsModel")

class MaterialsModel(Base):
    __tablename__ = "materials"
    material_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    material_name = Column(String, nullable=False)
    available_quantity = Column(Integer, nullable=False)
    measurement_unit = Column(String)

class Print3dModel(BudgetModel):
    __tablename__ = "print3d_budget"
    print3d_id = Column(Integer, primary_key=True, autoincrement=True)
    plastic_color = Column(String)
    layer_height = Column(Float)
    use_support = Column(Boolean)
    scale = Column(Float)
    infill_percent = Column(Integer)
    other_params = Column(String)

class LaserCutModel(BudgetModel):
    __tablename__ = "lasercut_budget"
    lasercut_id = Column(Integer, primary_key=True, autoincrement=True)
    operation_type = Column(Enum('engrave', 'cut', 'dotted'))
    scale = Column(Float)

class MakerMemberModel(Base):
    __tablename__ = "maker_member"
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    matricula = Column(String, nullable=False)
    cellphone_number = Column(String, nullable=False)
    id_area = Column(Integer, nullable=False, ForeignKey("area.area_id"))
    is_active = Column(Boolean, nullable=False, default=True)
    area = relationship("AreaModel")

class AreaModel(Base):
    area_id = Column(Integer, nullable=False, primary_key=True)
    description = Column(String, nullable=False)
    team_capitain_id = Column(Integer, nullable=False, ForeignKey("maker_member.user_id"))
    team_capitain = relationship("MakerMemberModel")




