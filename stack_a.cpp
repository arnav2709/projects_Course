#include <stdexcept>
#include "stack_a.h"
#include <iostream>
using namespace std;
Stack_A::Stack_A()
{   size=0;
}
void Stack_A::push(int data)
{   if(size==1024){
        throw runtime_error("Stack Full");
        }
    else{
        stk[size]=data;
        size+=1;
    }
}
int Stack_A::pop()
{
    if(size==0){
        throw runtime_error("Empty Stack");
    }
    else{
        int top=stk[size-1];
        size-=1;
        return top;
    }
}
int Stack_A::get_element_from_top(int idx)
{   if(idx>size-1){
        throw runtime_error("Index out of range");
        }
    else{
        return stk[size-idx-1];}
}
int Stack_A::get_element_from_bottom(int idx)
{   if(idx>size-1){
        throw runtime_error("Index out of range");
        }
    else{
        return stk[idx];}
}
void Stack_A::print_stack(bool top_or_bottom)
{
    if(! top_or_bottom){
        for(int i=0;i<size;i++){
        cout << stk[i] << endl;}
        }
    else{
        for(int i=size-1;i>=0;i--){
            cout << stk[i] << endl;  }
    }
}
int Stack_A::add()
{   if(size<2){
    throw runtime_error("Not enough Arguments");
    }
    else{
        int temp1=stk[size-1];
        int temp2=stk[size-2];size-=2;
        stk[size]=temp1+temp2;
        size+=1;
        return temp1+temp2;
            }
}
int Stack_A::subtract()
{   if(size<2){
        throw runtime_error("Not enough Arguments");
    }
    else{
        int temp1=stk[size-1];
        int temp2=stk[size-2];size-=2;
        stk[size]=temp2-temp1;
        size+=1;
        return temp2-temp1; }
}
int Stack_A::multiply()
{   if(size<2){
        throw runtime_error("Not enough Arguments");
    }
    else{
        int temp1=stk[size-1];
        int temp2=stk[size-2];size-=2;
        stk[size]=temp1*temp2;
        size+=1;
        return temp1*temp2;
            }
}

int Stack_A::divide()
{if(size<2){
        throw runtime_error("Not enough Arguments");
    }
    else{
        int temp1=stk[size-1];
        int temp2=stk[size-2];
        if(temp1==0){
            size-=2;
            throw runtime_error("Divide by Zero Error");}
        else{
            size-=2;
            double x=(temp2*1.0)/temp1;
            int ans=0;
            if (x >= 0) {
            ans=static_cast<int>(x);
            } 
            else {
                int intPart = static_cast<int>(x);
                ans = (x == intPart) ? intPart : intPart - 1;
    }
            stk[size]=ans;
            size+=1;
            return ans;}
        }
}

int *Stack_A::get_stack()
{
    return stk;
}

int Stack_A::get_size()
{
    return size;
}
