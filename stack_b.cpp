#include "stack_b.h"
#include <stdexcept>
#include <iostream>
using namespace std;
Stack_B::Stack_B()
{   stk=new int[1024];
    size=0;capacity=1024;
}
Stack_B::~Stack_B()
{   delete [] stk;
}
void Stack_B::push(int data){
  if(size==capacity){
    int newcapacity=capacity*2;
    int* temp=new(nothrow) int[newcapacity];
    if(!temp){
        throw runtime_error("Out of Memory");
        }
    for(int i=0;i<size;i++){
        temp[i]=stk[i]; }
    delete []stk;
    stk=temp;
    capacity=newcapacity;
    temp[size]=data;
    size++;}
    else{
        stk[size]=data;
        size+=1;
    }
}
int Stack_B::pop()
{   if(size==0){
    throw runtime_error("Empty Stack");}
    else{
        size-=1;
        int ans=stk[size];
        if(size<=(capacity/4) and capacity>=2048){
            int newcapacity=capacity/2;
            int* temp=new(nothrow) int[newcapacity];
            for(int i=0;i<size;i++){
                temp[i]=stk[i];   }
            delete []stk;
            stk=temp;
            capacity=newcapacity;
                }         
        return ans;
        }
        
}

int Stack_B::get_element_from_top(int idx)
{   if(idx>size-1){
        throw runtime_error("Index out of range");
        }
    else{
        return stk[size-idx-1];}
}

int Stack_B::get_element_from_bottom(int idx)
{
    if(idx>size-1){
        throw runtime_error("Index out of range");
        }
    else{
        return stk[idx];}
}

void Stack_B::print_stack(bool top_or_bottom)
{
    if(! top_or_bottom){
        for(int i=0;i<size;i++){
            cout << stk[i] << endl;
        }    }
    else{
        for(int i=size-1;i>=0;i--){
            cout << stk[i] << endl;        }
    }
}

int Stack_B::add()
{
        if(size<2){
            throw runtime_error("Not enough Arguments");
        }
        else{
            int temp1=stk[size-1];
            int temp2=stk[size-2];size-=2;
            stk[size]=temp1+temp2;
            size+=1;
            if(size<=(capacity/4) and capacity>=2048){
            int newcapacity=capacity/2;
            int* temp=new(nothrow) int[newcapacity];
            for(int i=0;i<size;i++){
                temp[i]=stk[i];   }
            delete []stk;
            stk=temp;
            capacity=newcapacity;
                }
            return temp1+temp2;
            }
        }
int Stack_B::subtract()
{
    if(size<2){
            throw runtime_error("Not enough Arguments");
        }
    else{
        int temp1=stk[size-1];
        int temp2=stk[size-2];size-=2;
        stk[size]=temp2-temp1;
        size+=1;
        if(size<=(capacity/4) and capacity>=2048){
        int newcapacity=capacity/2;
        int* temp=new(nothrow) int[newcapacity];
        for(int i=0;i<size;i++){
            temp[i]=stk[i];   }
        delete []stk;
        stk=temp;
        capacity=newcapacity;
            }
        return temp2-temp1;
            }

}

int Stack_B::multiply()
{
    if(size<2){
            throw runtime_error("Not enough Arguments");
        }
    else{
        int temp1=stk[size-1];
        int temp2=stk[size-2];size-=2;
        stk[size]=temp2*temp1;
        size+=1;
        if(size<=(capacity/4) and capacity>=2048){
        int newcapacity=capacity/2;
        int* temp=new(nothrow) int[newcapacity];
        for(int i=0;i<size;i++){
            temp[i]=stk[i];   }
        delete []stk;
        stk=temp;
        capacity=newcapacity;
            }
        return temp2*temp1;
            }
    
}

int Stack_B::divide()
{
    if(size<2){
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
            } else {
                int intPart = static_cast<int>(x);
                ans=(x == intPart) ? intPart : intPart - 1;
                }
            stk[size]=ans;
            size+=1;
            if(size<=(capacity/4) and capacity>=2048){
                int newcapacity=capacity/2;
                int* temp=new(nothrow) int[newcapacity];
                for(int i=0;i<size;i++){
                    temp[i]=stk[i];   }
                delete []stk;
                stk=temp;
                capacity=newcapacity;
                }
            return ans;
            }
        }
    
}

int *Stack_B::get_stack()
{
    return stk;
}

int Stack_B::get_size()
{
    return size;
}