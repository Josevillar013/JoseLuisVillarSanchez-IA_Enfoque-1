# Importar la librería pgmpy para trabajar con redes bayesianas
from pgmpy.models import DynamicBayesianNetwork as DBN
from pgmpy.factors.discrete import TabularCPD

# Crear una instancia de la DBN
dbn = DBN()

# Definir las variables del modelo
dbn.add_edges_from([(('Inventory', 0), ('Inventory', 1)), (('Demand', 0), ('Inventory', 1))])

# Definir las CPDs para las variables
cpd_inventory_0 = TabularCPD(variable='Inventory', variable_card=2, values=[[0.8, 0.2]])
cpd_demand_0 = TabularCPD(variable='Demand', variable_card=2, values=[[0.5, 0.5]])

cpd_inventory_1 = TabularCPD(variable='Inventory', variable_card=2, values=[[0.9, 0.1], [0.6, 0.4]], evidence=['Inventory'], evidence_card=[2])
cpd_demand_1 = TabularCPD(variable='Demand', variable_card=2, values=[[0.7, 0.3], [0.4, 0.6]], evidence=['Demand'], evidence_card=[2])

# Añadir las CPDs al modelo
dbn.add_cpds(cpd_inventory_0, cpd_demand_0, cpd_inventory_1, cpd_demand_1)

# Verificar la validez del modelo
assert dbn.check_model()

# Calcular la utilidad esperada de cada decisión
expected_utility_decision_0 = 0.8 * (0.5 * 0.8) + 0.2 * (0.5 * 0.2)
expected_utility_decision_1 = 0.9 * (0.1 * 0.3) + 0.1 * (0.9 * 0.7)

print("Utilidad esperada de Decision=0:", expected_utility_decision_0)
print("Utilidad esperada de Decision=1:", expected_utility_decision_1)