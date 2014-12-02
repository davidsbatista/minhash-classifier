__author__ = 'dsbatista'

classes = {"accuse(Arg1,Arg2)",
           "accuse(Arg2,Arg1)",
           "founded-by(Arg1,Arg2)",
           "founded-by(Arg2,Arg1)",
           "hold-shares-of(Arg1,Arg2)",
           "hold-shares-of(Arg2,Arg1)",
           "located-in(Arg1,Arg2)",
           "located-in(Arg2,Arg1)",
           "member-of(Arg1,Arg2)",
           "member-of(Arg2,Arg1)",
           "merged-with(Arg1,Arg2)",
           "owns(Arg1,Arg2)",
           "owns(Arg2,Arg1)",
           "studied-at(Arg1,Arg2)",
           "studied-at(Arg2,Arg1)",
           "support(Arg1,Arg2)",
           "support(Arg2,Arg1)",
           "works-with(Arg1,Arg2)"}

"""

########################
# EVALUATION EXPERIMENTS
#########################


def classify_sentences(data_file):
    with open(data_file) as f:
        total = sum(1 for _ in f)
    f.close()

    sentences = []
    f_sentences = codecs.open(data_file, encoding='utf-8')
    c = 0
    for line in f_sentences:
        c += 1
        if c % 10 == 0:
            print c, "/", total
        sentence = line.strip()

        # extract contexts (i.e., BEFORE,BETWEEN,AFTER) and entities types
        regex = re.compile('<[A-Z]+>[^<]+</[A-Z]+>', re.U)
        matches = []

        for m in re.finditer(regex, sentence):
            matches.append(m)

        for x in range(0, len(matches) - 1):
            if x == 0:
                start = 0
            if x > 0:
                start = matches[x - 1].end()

            try:
                end = matches[x + 2].start()
            except Exception, e:
                end = len(sentence) - 1

            before = sentence[start:matches[x].start()]
            between = sentence[matches[x].end():matches[x + 1].start()]
            after = sentence[matches[x + 1].end(): end]
            ent1 = matches[x].group()
            ent2 = matches[x + 1].group()

            arg1match = re.match('<[A-Z]+>', ent1)
            arg2match = re.match('<[A-Z]+>', ent2)

            arg1type = arg1match.group()[1:-1]
            arg2type = arg2match.group()[1:-1]

            # extract features
            features = extract_features(before, between, after, arg1type, arg2type)
            shingles = features.getvalue().strip().split(' ')

            # calculate min-hash sigs
            sigs = hashes.signature(shingles, N_SIGS)
            r = Relationship(0, sentence, None, shingles, sigs, arg1type, arg2type, ent1, ent2)
            sentences.append(r)

    return sentences

def evalute(results, class_relation):
    num_instances_of_class = 0
    num_correct_classified = 0
    num_classified = 0
    num_correct = 0
    precision = None
    recall = None
    f1 = None

    for r in results:
        rel_type = r[0]
        classified = r[1]

        if rel_type == class_relation:
            num_instances_of_class += 1
            if classified == rel_type:
                num_correct_classified += 1

        if classified == class_relation:
            num_classified += 1
        if rel_type == classified:
            num_correct += 1

        if num_classified == 0:
            precision = 0
        else:
            precision = (num_correct_classified / num_classified)

        if num_instances_of_class == 0:
            recall = 0
        else:
            recall = (num_correct_classified / num_instances_of_class)

        if precision == 0 and recall == 0:
            f1 = 0.0
        else:
            f1 = (2.0 * ((precision * recall) / (precision + recall)))

    print class_relation
    print "Precision :", precision
    print "Recall    :", recall
    print "F1        :", f1


def experiment_folds(relationships):
    # generate folds
    folds = generate_folds(relationships)
    average = dict()

    n_classes = dict()

    for r in relationships:
        if r.rel_type in n_classes:
            n_classes[r.rel_type] += 1
        else:
            n_classes[r.rel_type] = 1

    # train/test using the different folds
    for i in range(1, len(folds)):
        results = []

        print "\nStarting fold", i

        # create bands
        bands = create_lsh(N_BANDS, N_SIGS)

        train_data = []
        # all elements before 'i'
        for chunk in folds[:i]:
            for x in chunk:
                train_data.append(x)

        # all elements after 'i'
        for chunk in folds[i + 1:]:
            for x in chunk:
                train_data.append(x)

        test_data = folds[i]
        index(train_data, bands)
        print "Train data:  ", len(train_data)
        print "Test  data:  ", len(test_data)

        for r in test_data:
            classified = classify(r, bands)
            results.append((r.rel_type, classified))

        for c in classes:
            correct = 0
            total = 0
            for r in results:
                if r[0] == c:
                    total += 1
                    if r[0] == r[1]:
                        correct += 1
            if total > 0:
                if c in average:
                    average[c] += correct / float(total)
                else:
                    average[c] = correct / float(total)

    print "\nAccuracy:"
    for c in average:
        avg_accuracy = average[c] / float(FOLDS)
        if c.startswith("hold-shares-of"):
            print c + '\t',
        else:
            print c + '\t\t',
        if c.startswith("owns"):
            print '\t',
        print "%.2f" % avg_accuracy + " (" + str(+n_classes[c]) + ")"



# Train all instances except one, classify the only one left-over
def train_all():
    for i in range(0, len(relationships)):
        bands = createLSH(N_BANDS,N_SIGS)

        train_data = []
        # all elements before 'i'
        for e in relationships[:i]:
            train_data.append(e)
        # all elements after 'i'
        for e in relationships[i+1:]:
            train_data.append(e)

        test_data = relationships[i]
        train(train_data)
        rel = classify(test_data)
        if rel == test_data.rel_type:
            print relationships[i].sentence

def generate_folds(dataset):
    # generate folds
    fold_size = len(dataset) / FOLDS
    folds = [chunk for chunk in chunks(dataset, fold_size)]
    return folds

"""