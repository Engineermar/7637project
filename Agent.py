# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
# from PIL import Image

def findByProperty(d, prop):

    for objectName in d.objects:
        thisObject = d.objects[objectName]
        if prop in thisObject.attributes:
            return thisObject


def excludeByProperty(d, prop):

    for objectName in d.objects:
        thisObject = d.objects[objectName]
        if prop not in thisObject.attributes:
            return thisObject

def transformUtility(transformationDict, prop, obj1, obj2):

    if prop in obj1.objects.attributes and prop in obj2.attributes:
        if obj1.attributes[prop] == obj2.attributes[prop]:
            transformationDict[prop] = 'unchanged'
        else:
            transformationDict[prop] = obj1.attributes[prop] + '->' + obj2.attributes[prop]

def createSingleTransformationNetwork(object1, object2):

    transformation = {}

    for prop in ['shape', 'size', 'fill', 'angle']:
        transformUtility(transformation, prop, object1, object2)

    return transformation

def createDoubleTransformationNetwork(standardObjects, relationalObjects):

    standardTransformation = {}
    relationalTransformation = {}

    for prop in ['shape', 'size', 'fill', 'angle']:
        transformUtility(standardTransformation, prop, standardObjects[0], standardObjects[1])
        transformUtility(relationalTransformation, prop, relationalObjects[0], relationalObjects[1])

    return [standardTransformation, relationalTransformation]


def createSemanticNetwork(i, j):
    # construct a semantic network showing the transformation that occurred
    # between frame i -> j
    # only one shape, no need to match by attributes
    if len(i.objects) == 1 and len(j.objects) == 1:
        transformation = createSingleTransformationNetwork(i, j)
        return transformation

    # 2 shapes, need to match by attributes, e.g. 'inside', 'outside'
    else:

        relational_keyword = None
        relationalObjects = []
        standardObjects = []

        # get relational matches first
        for objectName in i.objects:
            thisObject = i.objects[objectName]

            for attributeName in thisObject.attributes:
                attributeValue = thisObject.attributes[attributeName]

                if attributeValue == 'inside':
                    relational_keyword = 'inside'
                    relationalObject = findByProperty(j, 'inside')
                    relationalObjects.append(thisObject)
                    relationalObjects.append(relationalObject)

        standardObjects.append(excludeByProperty(i, relational_keyword))
        standardObjects.append(excludeByProperty(j, relational_keyword))
        transformations = createDoubleTransformationNetwork(standardObjects, relationalObjects)
        return transformations


def agentCompare(init_network, solution_network):

    print('horizontal')
    print('a -> b')
    print(init_network[0])
    print('c -> solution')
    print(solution_network[1])
    print('\n')
    print('vertical')
    print('a -> c')
    print(init_network[1])
    print('b -> solution')
    print(solution_network[0])
    print('\n')

    shared_items1 = set(init_network[0].items()) & set(
        solution_network[1].items())

    shared_items2 = set(init_network[1].items()) & set(
        solution_network[0].items())

    print(str(len(shared_items1)) + ' matches horizontally')
    print(str(len(shared_items2)) + ' matches vertically')

    return len(shared_items1) + len(shared_items2)


class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().]

    def __init__(self):
        pass

    def Solve(self, problem):

        if problem.problemType == '3x3':
            return [.1, .1, .1, .1, .1, .1]

        if problem.name != 'Basic Problem B-01':
            return [.1, .1, .1, .1, .1, .1]

        a = problem.figures["A"]
        b = problem.figures["B"]
        c = problem.figures["C"]

        _1 = problem.figures["1"]
        _2 = problem.figures["2"]
        _3 = problem.figures["3"]
        _4 = problem.figures["4"]
        _5 = problem.figures["5"]
        _6 = problem.figures["6"]

        # generate our initial semantic network to test against
        init_network = [createSemanticNetwork(
            a, b), createSemanticNetwork(a, c)]

        # all possible solutions
        solutions = [_1, _2, _3, _4, _5, _6]
        scores = []

        for solution in solutions:

            # compare init_network with generated solutions
            solution_network = [createSemanticNetwork(
                c, solution), createSemanticNetwork(b, solution)]

            score = agentCompare(init_network, solution_network)
            scores.append(score)

        t = float(sum(scores))
        out = [x / t for x in scores]

        print(out)
        print('given answer: ' + str(scores.index(max(scores)) + 1))
        print('actual answer: ' + str(problem.checkAnswer(out)))

        return out
