#include "list.h"
#include <iostream>
using namespace std;
List::List()
{
     sentinel_head=new Node();
     sentinel_tail=new Node();
     sentinel_head->next=sentinel_tail;
     sentinel_tail->prev=sentinel_head;
     size=0;
}

List::~List()
{
    while(size>0){
        delete_tail();
    }
    delete sentinel_head;
    delete sentinel_tail;
    
}

void List::insert(int v)
{
    Node* n1=new(nothrow)Node(v,nullptr,nullptr);
    if(n1==nullptr){
        throw runtime_error("Out of Memory");
    }
    size+=1;
    sentinel_tail->prev->next=n1;
    n1->prev=sentinel_tail->prev;
    n1->next=sentinel_tail;
    sentinel_tail->prev=n1;
    
}

int List::delete_tail()
{   
    int value=sentinel_tail->prev->get_value();
    Node* n1=sentinel_tail->prev;
    n1->prev->next=sentinel_tail;
    sentinel_tail->prev=n1->prev;
    delete n1;
    size-=1;
    return value;
}

int List::get_size()
{
    return size;
}

Node *List::get_head()
{
    return sentinel_head;
}
