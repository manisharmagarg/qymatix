import sqlalchemy
import autogen_entities


database = 'data_qy___test_com'
database = 'data_clarus___films_com'

url = "mysql+mysqlconnector://root:dev@0.0.0.0:3306/{}".format(database)
engine = sqlalchemy.create_engine(
                url,
                connect_args={'use_pure': True}
            )

Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()



customers = session.query(autogen_entities.Customer).all()
for c in customers:
    print(c.name)

customer_name = 'BRAHMS DIAGNOSTIKA'
customer_industry = 'Medizin-Pharma'

customer_x = session.query(autogen_entities.Customer).filter_by(name=customer_name).first()

print(customer_x.industry)

customer_x.industry = customer_industry

session.commit()

print(">>>>")
print(customer_x.industry)


