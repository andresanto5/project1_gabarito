import sys
import argparse
from util import search
from util import db_index

def main():

    # Criar um objeto do pacote argparser
    parser = argparse.ArgumentParser(description="A Tool to index and search large multifasta files")

    # Para criar um subcomando, adicionar o metodo add_subparser
    subparsers = parser.add_subparsers(title='subcommands',
                                       description='valid subcommands',
                                       help='Use retrieve_seq.py {subcommand} -h for help with each subcommand'
                                       )

    ######## INDEX
    # Com o metodo add_parser, adicionar ao subcomando ao help do comando
    parser_index = subparsers.add_parser('index', help='Index all sequences in the database')

    # Adicionar os argumentos do subcomando
    parser_index.add_argument("--db", dest='db', default=None, action="store", help="A multifasta DB to be indexed",
                        required=False)

    ######## EXTRACT
    parser_extract = subparsers.add_parser('extract', help='Extract sequence in a multifasta')

    parser_extract.add_argument('-f', '--file', dest='file', action="store", help="A multifasta file",
                        required=False)

    parser_extract.add_argument('-e','--end', type=int,
                          help="end position on the fasta sequence",
                          required=False)

    parser_extract.add_argument('-s','--start', type=int,
                          help="start position on the fasta sequence",
                          required=False)

    parser_extract.add_argument('-g','--gene', type=str,
                          help="A gene (or chromossome) name",
                          required=False)

    parser_extract.add_argument('-l','--len', action='store_true',
                          help="Get the length of all genes. "
                               "If --gene get the length of the provided gene",
                          required=False)

    ######## SPLICE
    parser_splice = subparsers.add_parser('splice', help='Retrieve multiples intervals')

    parser_splice.add_argument('-f', '--file', dest='file', action="store", help="A multifasta file",
                        required=False)

    parser_splice.add_argument('-g','--gene', type=str,
                          help="A gene (or chromossome) name",
                          required=False)

    parser_splice.add_argument('-r', '--range',
                               dest='rg',
                               action='store',
                               nargs='+',
                               required=False,
                               help='Values in the form start-end space separated. 10-20 50-60 70-100')

    ########
    args = parser.parse_args()


    # function hasattr must be used because args may or may not have arg.db, and test it with just an
    # if args.db does not work

    if hasattr(args, 'db'):
        db_index.create_index(args.db)
        print("DB {db} has been indexed".format(db=args.db))


    if hasattr(args, 'start') and args.start is not None:   # args.start exists and has a value
        fasta = args.file
        start = args.start
        end = args.end
        gene_name = args.gene
        seq = search.search_seq(fasta, start, end, gene_name)

        print('>{gene}:{start}-{end}'.format(gene=gene_name,start=start,end=end))
        for i in seq:
            print(i)

    if hasattr(args, 'len') and args.len:   # arg.len is True
        fasta = args.file
        gene_name = args.gene if args.gene else None
        search.length(fasta, gene_name)


    if hasattr(args, 'rg') and args.rg is not None:  # args.start exists and has a value
        fasta = args.file
        gene_name = args.gene

        for interval in args.rg:
            gene_interval = interval.split('-')
            print('\n>{gene}:{start}-{end}'.format(gene=gene_name, start=gene_interval[0], end=gene_interval[1]))
            seq = search.search_seq(fasta, int(gene_interval[0]), int(gene_interval[1]), gene_name)
            for i in seq:
                print(i)


if __name__ == '__main__':
    main()

