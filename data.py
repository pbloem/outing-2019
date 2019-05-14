import rdflib as rdf
import gzip, os, wget, pickle

VALPROP = 0.4
REST = '.rest'
INV  = 'inv.'

DIR = os.path.dirname(os.path.realpath(__file__))

def load(name):
    """
    Loads a knowledge graph dataset. Self connections are automatically added as a special connection

    :param name: Dataset name ('aifb' or 'am' at the moment)
    :param final: If true, load the canonical test set, otherwise split a validation set off from the training data.
    :param limit: If set, the number of unique relations will be limited to this value, plus one for the self-connections,
                  plus one for the remaining connections combined into a single, new relation.
    :param bidir: Whether to include inverse links for each relation
    :return: A tuyple containing the graph data, and the classification test and train sets.
    """

    if name == 'aifb':
        # AIFB data (academics, affiliations, publications, etc. About 8k nodes)
        file = DIR + '/data/aifb_stripped.nt.gz'

    if name == 'eswc':
        # AIFB data (academics, affiliations, publications, etc. About 8k nodes)
        file = DIR + '/data/eswc-2017-complete.ttl'

    # if name == 'am':
    #     # Collection of the Amsterdam Museum. Data is downloaded on first load.
    #     data_url = 'https://www.dropbox.com/s/1mp9aot4d9j01h9/am_stripped.nt.gz?dl=1'
    #     file = DIR + '/data/am_stripped.nt.gz'
    #
    #     print('dataset file exists: ', os.path.isfile(file))
    #     if not os.path.isfile(file):
    #         print('Downloading AM data.')
    #         wget.download(data_url, file)
    #
    # elif name == 'bgs':
    #     file = DIR + '/data/bgs_stripped.nt.gz'
    #

    # -- Parse the data with RDFLib
    graph = rdf.Graph()

    if file.endswith('nt.gz'):
        with gzip.open(file, 'rb') as f:
            graph.parse(file=f, format='nt')
    else:
        graph.parse(file, format=rdf.util.guess_format(file))

    print('RDF loaded.')

    return graph
