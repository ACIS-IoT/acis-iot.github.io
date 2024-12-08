import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import graphviz
from sklearn.tree import export_text
from sklearn.preprocessing import LabelEncoder

target = 'C'
variable = ['D1H', 'D2H']

# Read the CSV dataset
df = pd.read_csv("gateway.csv")


# Save the categorized dataset to a file
df.to_csv('categorized_dataset.csv', index=False)

# Encode the categorical target variable into numerical labels
label_encoder = LabelEncoder()
df[target] = label_encoder.fit_transform(df[target])

# Split the dataset into features (variable) and target (target)
X = df[['D1H', 'D2H']]
y = df[target]

# Initialize the decision tree classifier with balanced class weights
clf = DecisionTreeClassifier(criterion='entropy')

# Train the classifier on the dataset
clf.fit(X, y)

# Visualize the decision tree
dot_data = tree.export_graphviz(clf,
                               out_file=None,
                               feature_names=X.columns,
                               filled=True,
                               rounded=True,
                               special_characters=True)
graph = graphviz.Source(dot_data)
graph.render("decision_tree", format="png", cleanup=True)

# Convert the decision tree to text format
tree_text = export_text(clf, feature_names=X.columns, show_weights=True)

print(tree_text)


tree = clf.tree_

ruleId = 0




def learn_prism_commands(occurence, at, class_label):
    global ruleId  # Declare 'ruleId' as a global variable to modify its value

    at = at.rsplit("&", 1)[0].strip()
    print(at)
    propb = 1/occurence
    npropb = 1 -propb
    merged_left = at
    RIGHT = []

    RIGHT.append('('+str(propb) + '):(' + target + "'=" + str(class_label) + ') +  ('+ str(npropb)+'): (' + target + "'=NOTDEFINED"')')

    separator = " + "  # Specify the separator you want to use
    merged_right = separator.join(RIGHT)

    ruleId += 1  # Increment the value of 'ruleId'

    return f"[rule{ruleId}] {merged_left} -> {merged_right};"




def learn_const_prism_module_variable( ):
    const_declarations=[]
    const_declarations.append('const int NOTDEFINED =-1;')
    for variable_name in variable:
            const_declarations.append(f"const double {variable_name};")  # Declare each variable as a constant double
    return const_declarations

def learn_prism_module_variable( nb):
    list_of_variable=[]
    list_of_variable.append(target + ' : [NOTDEFINED..'+str(nb[0])+'] init 0 ;')
    return list_of_variable
listOfCommands=[]
# Define a function to recursively traverse the decision tree and calculate weighted probability
def traverse_tree(node_id=0, depth=0, parent_probability=1.0, at=""):
    indent = "  " * depth
    if tree.feature[node_id] != -2:  # If not a leaf node
        feature = tree.feature[node_id]
        threshold = tree.threshold[node_id]
        #print(tree.feature[node_id])
        at_left = at + variable[feature] + "<=" + str(threshold) +" & "
        traverse_tree(tree.children_left[node_id], depth + 1, parent_probability * tree.weighted_n_node_samples[node_id] / tree.weighted_n_node_samples[0], at_left)

        at_right = at + variable[feature]+ ">"+ str(threshold) +" & "
        traverse_tree(tree.children_right[node_id], depth + 1,  parent_probability * tree.weighted_n_node_samples[node_id] / tree.weighted_n_node_samples[0], at_right)
    else:  # If a leaf node
        leaf_node_weight = tree.weighted_n_node_samples[node_id]
        weights = tree.value[node_id]  # Access weights directly
        class_label = np.argmax(weights)
        listOfCommands.append(learn_prism_commands(leaf_node_weight,at,class_label))


MODELNAME ="mdp "
MODULE ="module GeneratedDecisiontree"
ENDMODULE="endmodule"
list_of_variable=learn_prism_module_variable (tree.n_classes)
list_of_const_variable=learn_const_prism_module_variable()
traverse_tree( )






file = open("tree.nm", "w")

file.write(MODELNAME + '\n \n')

for elt in list_of_const_variable:
    file.write(elt + '\n')



file.write(MODULE + '\n')
for elt in list_of_variable:
    file.write(elt + '\n')

for elt in listOfCommands:
    file.write(elt + '\n')
file.write(ENDMODULE + '\n')




# Close the file
file.close()