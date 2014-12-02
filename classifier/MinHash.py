import sys
import scipy
import xxhash

MAX_32_INT = sys.maxint


def signature(shingles, n_sigs):
    ret = scipy.zeros(n_sigs)
    for function_id in xrange(n_sigs):
        ret[function_id] = min_hash(shingles, function_id)
    return ret


def min_hash(shingles, function_id):
    minhash = MAX_32_INT
    for shingle in shingles:
        hash_value = hash_function(shingle, function_id)
        if hash_value < minhash:
            minhash = hash_value
    return minhash


def hash_function(shingle, function_id):
    #return hash(shingle * function_id * function_id)
    return hash(shingle * function_id)
    #return xxhash.xxh32(shingle.encode("utf8") * function_id * function_id).intdigest()