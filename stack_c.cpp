#include "stack_c.h"
#include<iostream>
#include<stdexcept>
using namespace std;
Stack_C::Stack_C()
{
    stk=new List();
}

Stack_C::~Stack_C()
{
    delete stk;
}

void Stack_C::push(int data)
{
    stk->insert(data);
}

int Stack_C::pop()
{
    if(stk->get_size()==0){
        throw runtime_error("Empty Stack");
    }
    else{
        int t=stk->delete_tail();
        return t;
    }
}

int Stack_C::get_element_from_top(int idx)
{   
    if(idx > stk->get_size()-1){
        throw runtime_error("Index out of range");
        }
    else{
    Node* head=stk->get_head();
    head=head->next;
    while(!(head->is_sentinel_node())){
        head=head->next;
    }
    int c=-1;
    while(c != idx){
        head=head->prev;
        c++;
    }
    return head->get_value();
    }
}

int Stack_C::get_element_from_bottom(int idx)
{   
    if(idx > stk->get_size()-1){
        throw runtime_error("Index out of range");
        }
    else{
    Node* head=stk->get_head();
    int c=-1;
    while(c != idx){
        head=head->next;
        c++;    }
    return head->get_value();}
}

void Stack_C::print_stack(bool top_or_bottom)
{
    if(  ! top_or_bottom){
        Node* head=stk->get_head();
        head=head->next;
        while( !(head->is_sentinel_node())){
            cout << head->get_value() << endl;
            head=head->next;
            }    }
    else{
        Node* head=stk->get_head();
    head=head->next;
    while(!(head->is_sentinel_node())){
        head=head->next;    }
    head=head->prev;
    while( !(head->is_sentinel_node())){
            cout << head->get_value() << endl;
            head=head->prev;
            }  
    }
}

int Stack_C::add()
{
    if(stk->get_size()<2){
        throw runtime_error("Not Enough Arguments");
    }
    else{
        int v1=stk->delete_tail();int v2=stk->delete_tail();
        int t=v1+v2;
        stk->insert(t);
        return t;
    }
   
}

int Stack_C::subtract()
{   if(stk->get_size()<2){
        throw runtime_error("Not Enough Arguments");
    }
    else{
        int v1=stk->delete_tail();int v2=stk->delete_tail();
        stk->insert(v2-v1);
        return v2-v1;
    }
    
}

int Stack_C::multiply()
{
    if(stk->get_size()<2){
        throw runtime_error("Not Enough Arguments");
    }
    else{
        int v1=stk->delete_tail();int v2=stk->delete_tail();
        stk->insert(v1*v2);
        return v2*v1;
    }
    
}

int Stack_C::divide()
{
    if(stk->get_size()<2){
        throw runtime_error("Not Enough Arguments");
    }
    else{
        int v1=stk->delete_tail();int v2=stk->delete_tail();
        if(v1==0){
            throw runtime_error("Divide by Zero Error");
        }
        else{
            double x=v2*(1.0)/v1;
            int ans=0;
            if (x >= 0) {
                ans=static_cast<int>(x);
            } else {
                int intPart = static_cast<int>(x);
                ans=(x == intPart) ? intPart : intPart - 1;
                }
            stk->insert(ans);
            return ans;
        }
    }
    
}

List *Stack_C::get_stack()
{
    return stk;
}

int Stack_C::get_size()
{
    return stk->get_size();
}
