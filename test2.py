#!/usr/bin/python
import os, sys, time
import math, random
from multiprocessing import Process, Manager

# a wrapper function which appends the result of "merge_sort" to the "responses" list
def merge_sort_multi(list_part):
    responses.append(merge_sort(list_part))


# a wrapper function which appends the result of "merge" to the "responses" list
def merge_multi(list_part_left, list_part_right):
    responses.append(merge(list_part_left, list_part_right))


# explained earlier
def merge_sort(a):
    length_a = len(a)
    if length_a <= 1: return a
    m = int(math.floor(length_a / 2))
    a_left = a[0:m]
    a_right = a[m:]
    a_left = merge_sort(a_left)
    a_right = merge_sort(a_right)
    return merge(a_left, a_right)


# ... also explained earlier
def merge(left, right):
    a = []
    while len(left) > 0 or len(right) > 0:
        if len(left) > 0 and len(right) > 0:
            if left[0] <= right[0]:
                a.append(left.pop(0))
            else:
                a.append(right.pop(0))
        elif len(left) > 0:
            a.extend(left)
            break
        elif len(right) > 0:
            a.extend(right)
            break
    return a


if __name__ == '__main__':
    try:
        cores = int(sys.argv[1])  # get the number of cores
        if cores > 1:
            if cores % 2 != 0:  # restrict core count to even numbers
                cores -= 1
        print 'Using %d cores' % cores
    except:
        cores = 16

    '''instantiate a multiprocessing.Manager object to store the output of each process,
    see example here http://docs.python.org/library/multiprocessing.html#sharing-state-between-processes '''
    manager = Manager()
    responses = manager.list()

    # randomize the length of our list
    l = random.randint(10 ** 5,10 ** 6)
    print 'List length : ', l

    # create an unsorted list with random numbers
    start_time = time.time()
    a = [random.randint(0, 100) for n in range(0, l)]
    print(a[:5])
    print 'Random list generated in ', time.time() - start_time
    # start timing the single-core procedure
    start_time = time.time()
    single = merge_sort(a)
    single_core_time = time.time() - start_time
    a_sorted = a[:]
    a_sorted.sort()
    ''' comparison with Python list's "sort" method, validation of the algorithm
    (it has to work right, doesn't it??) '''
    print 'Verification of sorting algorithm', a_sorted == single
    print 'Single Core: %4.6f sec' % ( single_core_time )
    if cores > 1:
        ''' we collect the list element count and the time taken
        for each of the procedures in a file '''
        f = open('mergesort-' + str(cores) + '.dat', 'a')
        print 'Starting %d-core process' % cores
        start_time = time.time()
        # divide the list in "cores" parts
        step = int(math.floor(l / cores))
        offset = 0
        p = []
        for n in range(0, cores):
            ''' we create a new Process object and assign the "merge_sort_multi" function to it,
            using as input a sublist '''
            if n < cores - 1:
                proc = Process(target=merge_sort_multi, args=( a[n * step:(n + 1) * step], ))
            else:
                # get the remaining elements in the list
                proc = Process(target=merge_sort_multi, args=( a[n * step:], ))
            p.append(proc)

        ''' http://docs.python.org/library/multiprocessing.html#multiprocessing.Process.start &
        http://docs.python.org/library/multiprocessing.html#multiprocessing.Process.join each Process '''
        for proc in p:
            proc.start()
        ''' Corrected! '''
        for proc in p:
            proc.join()
        print 'Performing final merge...'
        start_time_final_merge = time.time()
        p = []
        ''' For a core count greater than 2, we can use multiprocessing
        again to merge sublists in parallel '''
        if len(responses) > 2:
            while len(responses) > 0:
                ''' we remove sublists from the "responses" list and pass it as input to the
                "merge_multi" wrapper function of "merge" '''
                proc = Process(target=merge_multi, args=(responses.pop(0), responses.pop(0)))
                p.append(proc)
            # again starting and joining ( this seems like a pattern, doesn't it ... ? )
            for proc in p:
                proc.start()
            for proc in p:
                proc.join()
        # finally we have 2 sublists which need to be merged
        a = merge(responses[0], responses[1])
        # ... anddd time!
        final_merge_time = time.time() - start_time_final_merge
        print 'Final merge duration : ', final_merge_time
        multi_core_time = time.time() - start_time
        # of course we double-check that we did everything right
        print 'Sorted arrays equal : ', (a == single)
        print '%d-Core ended: %4.6f sec' % (cores, multi_core_time)
        # we write down the results in our log file
        f.write("%d %4.3f %4.3f %4.2f %4.3f\n" % (
        l, single_core_time, multi_core_time, multi_core_time / single_core_time, final_merge_time))
        f.close()