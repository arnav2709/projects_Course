#include "node.h"

Node::Node(bool sentinel)
{   
    prev=nullptr;
    next=nullptr;
}

Node::Node(int v, Node *nxt, Node *prv)
{
    value=v;next=nxt;prev=prv;
}

bool Node::is_sentinel_node()
{
    if(prev==nullptr || next==nullptr){
        return true;
    }
    return false;
    
}

int Node::get_value()
{
    return value;
}
