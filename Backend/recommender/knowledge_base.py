import numpy as np
import copy

# Adults:

# Histidine: 10
# Isoleucine: 20
# Leucine: 39
# Lysine: 30
# MethioninePlusCysteine: 15 (sulfur amino acids)
# PhenylalinePlusTyrosine: 25 (aromatic amino acids)
# Threonine: 15
# Tryptophan: 4
# Valine: 26

# sulfur devided
# Methionine: 10.4
# Cysteine: 4.1

class WhoPattern():

    def __init__(self,
                 histidine = 0,
                 isoleucine = 0,
                 leucine = 0,
                 lysine = 0,
                 methionine_plus_cysteine = 0,
                 phenylalanine_plus_tyrosine = 0,
                 threonine = 0,
                 tryptophan = 0,
                 valine = 0):
        self.histidine = histidine
        self.isoleucine = isoleucine
        self.leucine = leucine
        self.lysine = lysine
        self.methionine_plus_cysteine = methionine_plus_cysteine
        self.phenylaline_plus_tyrosine = phenylalanine_plus_tyrosine
        self.threonine = threonine
        self.tryptophan = tryptophan
        self.valine = valine

    def to_list(self):
        fields_dict = self.__dict__
        return list(fields_dict.values())
        

    def to_np_array(self):
        fields_values_list = self.to_list()
        return np.array(fields_values_list)

    def get_fields_keys(self):

        members_keys_list = list(self.__dict__.keys())
        return members_keys_list

    def mult_scalar(self, scalar):

        return_pattern = copy.deepcopy(self)

        for current_nutrient_str, current_amount in return_pattern.__dict__.items():
            return_pattern.__setattr__(current_nutrient_str, current_amount * scalar)
        return return_pattern

    def add_pattern(self, other_nutrients_pattern):

        return_pattern = copy.deepcopy(self)

        for current_nutrient_str, current_amount in return_pattern.__dict__.items():
            return_pattern.__setattr__(current_nutrient_str, current_amount + other_nutrients_pattern.__getattribute__(current_nutrient_str))

        return return_pattern

    def sub_scalar(self, scalar):

        return_pattern = copy.deepcopy(self)

        for current_nutrient_str, current_amount in return_pattern.__dict__.items():
            return_pattern.__setattr__(current_nutrient_str, current_amount - scalar)

        return return_pattern


    def div_pattern(self, other_nutrients_pattern):

        return_pattern = copy.deepcopy(self)

        for current_nutrient_str, current_amount in return_pattern.__dict__.items():
            return_pattern.__setattr__(current_nutrient_str, current_amount / other_nutrients_pattern.__getattribute__(current_nutrient_str))

        return return_pattern

    def mean(self):

        sum = 0.0

        for current_amount in self.__dict__.values():
            sum += current_amount

        return sum / len(self.__dict__)
    
    def mean_deviation(self):

        normalized_pattern = self * (1 / self.mean())

        return normalized_pattern - 1

    def mean_square_sum(self):

        return sum(self.mean_deviation**2)


    def __mul__(self, factor):

        return self.mult_scalar(factor)

    def __rmul__(self, factor):

        return self.mult_scalar(factor)
    
    def __add__(self, other):

        return self.add_pattern(other)

    def __radd__(self, other):

        return self.add_pattern(other)

    def __truediv__(self, other):

        return self.div_pattern(other)

    def __sub__(self, scalar):

        return self.sub_scalar(scalar)

    def __rsub__(self, scalar):

        return self.sub_scalar(scalar) * (-1)
    

    def __str__(self):
        ret_str = ''
        for current_nutrient_str, current_amount in self.__dict__.items():
            ret_str = ret_str + current_nutrient_str + ': ' + '%.2f' % current_amount + '\n'

        return ret_str


# tissue_requirements_pattern = NutrientsPattern(27, 35, 75, 73, 35, 73, 42, 12, 49)
# maintainance_requirements_pattern = NutrientsPattern(15, 30, 59, 45, 22, 38, 23, 6, 39)

tissue_requirements_pattern = np.array([27, 35, 75, 73, 35, 73, 42, 12, 49]) / 1000.0

maintainance_requirements_pattern = np.array([15, 30, 59, 45, 22, 38, 23, 6, 39]) / 1000.0

tissue_factors = {
    'age':      [0.5,  1,   3,    15,   18],
    'factor':   [0.46, 0.2, 0.07, 0.04, 0.0]
}

maintanance_factor = 0.66

def calculate_requirements(age, weight_kg):
    tissue_factor = np.interp(age, tissue_factors['age'], tissue_factors['factor'])
    requirements_per_kg_mg = tissue_requirements_pattern * tissue_factor + maintainance_requirements_pattern * maintanance_factor
    return requirements_per_kg_mg * weight_kg

def calculate_normalized_intake_from_requiremts(intake_pattern, absolute_requirements):
    return intake_pattern / absolute_requirements

def calculate_normalized_intake(intake_pattern, age, weight_kg):
    return calculate_normalized_intake_from_requiremts(intake_pattern, calculate_requirements(age, weight_kg))


def calculate_realtive_balance(intake_pattern):

    mean = intake_pattern.mean()

    return mean

def calculate_who_patterns(food_amino_acids_dicts):

    who_patterns_lists = []
    for current_food_amino_acids_dict in food_amino_acids_dicts:
        current_pattern = WhoPattern(
            histidine = current_food_amino_acids_dict["Histidine"],
            isoleucine = current_food_amino_acids_dict["Isoleucine"],
            leucine = current_food_amino_acids_dict["Leucine"],
            lysine = current_food_amino_acids_dict["Lysine"],
            methionine_plus_cysteine = current_food_amino_acids_dict["Methionine"] + current_food_amino_acids_dict["CystEine"] ,
            phenylalanine_plus_tyrosine = current_food_amino_acids_dict["Phenylalanine"] + current_food_amino_acids_dict["Tyrosine"],
            threonine = current_food_amino_acids_dict["Threonine"],
            tryptophan = current_food_amino_acids_dict["Tryptophan"],
            valine = current_food_amino_acids_dict["Valine"]
        )
        who_patterns_lists.append(current_pattern.to_list())

    return who_patterns_lists


def get_who_pattern_keys():
    return WhoPattern().get_fields_keys()

# print(tissue_requirements_pattern / maintainance_requirements_pattern)

# print(calculate_requirements(40, 85).__str__())

# print(tissue_requirements_pattern)

# print(calculate_realtive_balance(tissue_requirements_pattern))
# print(tissue_requirements_pattern)
# print(maintainance_requirements_pattern)

# maintainance_requirements_pattern

#print(tissue_requirements_pattern.mean_deviation())