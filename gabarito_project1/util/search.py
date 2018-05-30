import pickle

def search_seq(fasta, start, end, gene_name):
    index = pickle.load(open(fasta + '.fai', 'rb'))

    seq = ''

    with open(fasta, 'r') as file:
        for line_num, line in enumerate(file, 1):

            line = line.strip()
            # Se o nome do gene esta presente no dicionario e
            # se a linha atual do loop esta presente no dict
            if line_num in index[gene_name].keys():

                # Se o start fornecido esta nesta linha
                if start >= index[gene_name][line_num][0] and start <= index[gene_name][line_num][1]:
                    start_pos = start - index[gene_name][line_num][0]

                    # Se o end tambem esta nesta linha
                    if end <= index[gene_name][line_num][1]:
                        end_pos = end + index[gene_name][line_num][0] - 1
                        seq = line[start_pos:end_pos]
                        yield seq
                        break

                    # Se o end esta em outra linha
                    elif end > index[gene_name][line_num][1]:
                        seq = line[start_pos:]

                # Se o comeco do gene esta em outra linha e o fim
                # pode ou nao estar na mesma linha
                if start < index[gene_name][line_num][0]:

                    if end > index[gene_name][line_num][1]:
                        seq = line[:]


                    elif end <= index[gene_name][line_num][1]:
                        end_pos = end - index[gene_name][line_num][0]
                        seq = line[:end_pos]
                        yield seq
                        break

            # Apenas um dos if sera verdadeiro. Isso quer dizer que ou a sequencia estara
            # completa na linha avaliada ou estara em multiplas linhas
                # No primeiro caso, a sequencia completa devera ser retornada e por isso o yield
                # devera retornar a sequencia e dar um break no for.

                # O segundo caso eh quando a sequencia esta em multiplas linhas. Assim, para cada loop,
                # devera ser retornado um generator para cada sequencia da linha. Ainda nesta condicao,
                # se houver algo atribuido na variavel seq, ele retornara ogenerator do seq.
            if len(seq) > 0:
                yield seq

def length(fasta, gene_name=None):
    index = pickle.load(open(fasta + '.fai', "rb"))

    if gene_name is None:

        for name in index.keys():
            last_index_line = sorted(index[name].keys())[-1] # key of the last line of the index file
            print(name, index[name][last_index_line][1])

    # Get the index[1] of the last tuple of the last line
    else:
        last_index_line = sorted(index[gene_name].keys())[-1]
        print(gene_name, index[gene_name][last_index_line][1])
























