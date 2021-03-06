

# ENCODINGS; One-Hot encoding would be preferred, but does not work with svm afaik
WORK_CLASS_INDEX = 1
EDUCATION_INDEX = 3
MARITAL_STATUS_INDEX = 5
OCCUPATION_INDEX = 6
RELATIONSHIP_INDEX = 7
RACE_INDEX = 8
SEX_INDEX = 9
NATIVE_COUNTRY_INDEX = 13
CATEGORICAL_INDECES = [WORK_CLASS_INDEX, EDUCATION_INDEX, MARITAL_STATUS_INDEX, OCCUPATION_INDEX, RELATIONSHIP_INDEX, RACE_INDEX, SEX_INDEX, NATIVE_COUNTRY_INDEX]
WORK_CLASS = {'Private': 1.0, 'Self-emp-not-inc': 2.0, 'Self-emp-inc': 3.0, 'Federal-gov': 4.0, 'Local-gov': 5.0, 'State-gov': 6.0, 'Without-pay': 7.0, 'Never-worked': 8.0}
EDUCATION = {'Bachelors': 1.0, 'Some-college': 2.0, '11th': 3.0, 'HS-grad': 4.0, 'Prof-school': 5.0, 'Assoc-acdm': 6.0, 'Assoc-voc': 7.0, '9th': 8.0, '7th-8th': 9.0, '12th': 10.0, 'Masters': 11.0, '1st-4th': 12.0, '10th': 13.0, 'Doctorate': 14.0, '5th-6th': 15.0, 'Preschool': 16.0}
MARITAL_STATUS = {'Married-civ-spouse': 1.0, 'Divorced': 2.0, 'Never-married': 3.0, 'Separated': 4.0, 'Widowed': 5.0, 'Married-spouse-absent': 6.0, 'Married-AF-spouse': 7.0}
OCCUPATION = {'Tech-support': 1.0, 'Craft-repair': 2.0, 'Other-service': 3.0, 'Sales': 4.0, 'Exec-managerial': 5.0, 'Prof-specialty': 6.0, 'Handlers-cleaners': 7.0, 'Machine-op-inspct': 8.0, 'Adm-clerical': 9.0, 'Farming-fishing': 10.0, 'Transport-moving': 11.0, 'Priv-house-serv': 12.0, 'Protective-serv': 13.0, 'Armed-Forces': 14.0}
RELATIONSHIP = {'Wife': 1.0, 'Own-child': 2.0, 'Husband': 3.0, 'Not-in-family': 4.0, 'Other-relative': 5.0, 'Unmarried': 6.0}
RACE = {'White': 1.0, 'Asian-Pac-Islander': 2.0, 'Amer-Indian-Eskimo': 3.0, 'Other': 4.0, 'Black': 5.0}
SEX = {'Female': -1.0, 'Male': 1.0}
NATIVE_COUNTRY = {'United-States': 1.0, 'Cambodia': 2.0, 'England': 3.0, 'Puerto-Rico': 4.0, 'Canada': 5.0, 'Germany': 6.0, 'Outlying-US(Guam-USVI-etc)': 7.0, 'India': 8.0, 'Japan': 9.0, 'Greece': 10.0, 'South': 11.0, 'China': 12.0, 'Cuba': 13.0, 'Iran': 14.0, 'Honduras': 15.0, 'Philippines': 16.0, 'Italy': 17.0, 'Poland': 18.0, 'Jamaica': 19.0, 'Vietnam': 20.0, 'Mexico': 21.0, 'Portugal': 22.0, 'Ireland': 23.0, 'France': 24.0, 'Dominican-Republic': 25.0, 'Laos': 26.0, 'Ecuador': 27.0, 'Taiwan': 28.0, 'Haiti': 29.0, 'Columbia': 30.0, 'Hungary': 31.0, 'Guatemala': 32.0, 'Nicaragua': 33.0, 'Scotland': 34.0, 'Thailand': 35.0, 'Yugoslavia': 36.0, 'El-Salvador': 37.0, 'Trinadad&Tobago': 38.0, 'Peru': 39.0, 'Hong': 40.0, 'Holand-Netherlands': 41.0}


def numerify_feature(feature, index):
    feature = feature.strip()
    if feature == '?':
        return 0.0

    elif index == WORK_CLASS_INDEX:
        return WORK_CLASS[feature]
    elif index == EDUCATION_INDEX:
        return EDUCATION[feature]
    elif index == MARITAL_STATUS_INDEX:
        return MARITAL_STATUS[feature]
    elif index == OCCUPATION_INDEX:
        return OCCUPATION[feature]
    elif index == RELATIONSHIP_INDEX:
        return RELATIONSHIP[feature]
    elif index == RACE_INDEX:
        return RACE[feature]
    elif index == SEX_INDEX:
        return SEX[feature]
    elif index == NATIVE_COUNTRY_INDEX:
        return NATIVE_COUNTRY[feature]

    return float(feature)


def extract_features(line_array):
    """
        Given a line of the input csv as an array of values.
        Return the features of the line (all but the last value) with
            numerical values substituted for categorical.
    """
    features = line_array[:-1]
    return [numerify_feature(features[i], i) for i in range(len(features))]


def extract_category(line_array):
    """
        Given a line of the input csv as an array of values.
        Compare the last value (the category) and return
            -1.0 if income is less than or equal to 50k
            1.0  if income is greater than 50k
    """
    neg_cat = "<=50K"
    category = line_array[-1].strip()
    return -1.0 if category == neg_cat else 1.0


def transform_input(_, line):
    line_array = line.split(',')
    features = extract_features(line_array)
    category = extract_category(line_array)
    return category, features
