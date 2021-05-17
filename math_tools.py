"""
module that holds a couple of mathematical tools
"""

import numpy as np

def polynomial_interpolation_newton_algorithm(x,y):
    """
    task: interpolate a polynoomial from given values using the newton algorithm \n
    parameters: x(list(float or int)), y(list(float or int))
    return value: list[float(coefficients of the interpolated function starting at b0,b1,b2,...,bn-1 with n= len(x))]
    """
    
    get_divided_difference= lambda y2,y1,x2,x1: (y2-y1)/ (x2-x1)
    divided_differences=[]
    coefficients=[]

    #store first coefficient manually as that is just y0
    divided_differences.append([])  #this list will not be used, but is there to get an intuitive indexing
    coefficients.append(y[0])

    # get the n coefficients, by iteratirng over each given point as row
    for row in range(1,len(x)):
        #start an empty list for each row to store the divided differences
        divided_differences.append([])

        #calculate the first divided difference for each row without a loop, cuz it does not use any other divided differences for calculation
        divided_differences[row].append(get_divided_difference(y[row],y[row-1],x[row],x[row-1])) #this will ba saved at [row,0]
        
        #calculate the other divided differences with loop
        for col in range(1,row):
            y2=divided_differences[row][col-1]
            y1=divided_differences[row-1][col-1]
            x2=x[row]
            x1=x[row-(col+1)]
            divided_differences[row].append(get_divided_difference(y2,y1,x2,x1)) #this will be saved at [row,col]

        #append the last divided_difference of each row to the coefficients list
        coefficients.append(divided_differences[row][row-1])

    #so these coefficients a will have the following meaning:
    #f(x)=a0+a1*(x-x1)+a2*(x-x1)*(x-x2)+a3*(x-x1)*(x-x2)*(x-x3) etc.
    #but we want sth like this:
    #f(x)=b0+b1*x+b2*x^2+b3*x^3 etc. so do this transformation in the following

    #calculate the final coefficients
    coefficient_table=[]
    coefficient_table.append([1])        #([coefficients[0]]) #append the first coefficient manually
    for row in range(1,len(coefficients)):
        
        #take the previous row, shift each place one to the right
        temp1_row=[0]+coefficient_table[row-1]

        #take the previous row and multiply each element by x[row-1]
        temp2_row=[el*x[row-1] for el in coefficient_table[row-1] ]+[0] #append this 0 so that temp1_row and temp2_row are of same length

        #take the columnwise difference of temp1_row and remp2_row and use that as the new row
        col_dif_row=[temp1_row[i]-temp2_row[i] for i in range(len(temp1_row))]
        coefficient_table.append(col_dif_row)   #this will be saved at coefficient_table[row]

    #this table now contains in each row the result of: (x-x0)*(x-x1)*(x-x2)*...*(x-x[row-1])
    #this has to be rowwise multiplied by the corresponding coefficients
    for row in range(len(coefficients)):
        for col in range(len(coefficient_table[row])):
            coefficient_table[row][col]*=coefficients[row]

    #do columnwise summation of the coefficient table, the results are the coefficients of the interpolated function
    final_coefficients=[]
    for col in range(len(coefficients)):
        curr_sum=0
        starting_row=col
        for row in range(starting_row,len(coefficients)):
            curr_sum+=coefficient_table[row][col]
        final_coefficients.append(curr_sum)

    return final_coefficients

def use_polynomial(coefficients,x):
    """
    task: evaluate the polynomial described by the coefficients at place x
    parameters: coefficients(list[float(coefficients of polynomial starting at b0,b1,b2,...)]), x(float(place at which polynomial will be evaluated))
    return value: float(value of given polynomial at place x)
    """

    degree=0
    total=0
    for coef in coefficients:
        total+= coef*pow(x,degree)
        degree+=1
    return total
    
def differantiate_polynomial(coefficients):
    """
    task: differantiate the polynomial described by the coefficients
    parameters: coefficients(list[float(coefficients of polynomial starting at b0,b1,b2,...)])
    return value: coefficients(list[float(coefficients of polynomial after differentiation starting at c0,c1,c2,...)])
    """

    degree=1
    differentiated_coefficients=[]
    for coef in coefficients[1:]:
        differentiated_coefficients.append(coef*degree)
        degree+=1

    return differentiated_coefficients


#test
"""
x=[1,2,3,4]
y=[1,4,9,16]
x_hat=2.5
coefs=polynomial_interpolation_newton_algorithm(x,y)
print(coefs)
print(differantiate_polynomial(coefs))
print(use_polynomial(coefs, x_hat))
"""