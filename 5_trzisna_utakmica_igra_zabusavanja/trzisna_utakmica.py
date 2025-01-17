from random import uniform


DISCOUNT = 1 - 0.1



D = 1000
A = [[0], [0]]

C  = [ 100, 95 ]
def c(i):
    var_material_price = C[i] *  uniform(0.9, 1.1)
    return var_material_price if A[i][-1] < 1000 else var_material_price * DISCOUNT

def calculate_a(i):
    a = round((D - sum(A[0]) - sum(A[1]) + sum(A[i]) - c(i)) / 2)
    return a if a > 0 else 0


def p(i):
    return D - A[i][-1]

def u(i):
    u =  round(p(i) * A[i][-1] - c(i)) 
    return u if u > 0 else 0


if __name__ == "__main__":

    for _ in range( 10 ):
        a1 = calculate_a(0)
        a2 = calculate_a(1)

        print('a1= ', a1)
        print('a2= ', a2)

        A[0].append(a1)
        A[1].append(a2)

        u1 = u(0)
        u2 = u(1)
        print('u1 = {} , u2 = {}, u1+u2 = {} \n'.format( u1, u2, u1+u2))
