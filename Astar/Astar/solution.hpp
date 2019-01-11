#ifndef _SOLUTION_HPP_
#define _SOLUTION_HPP_

#include "status.hpp"
#include <queue>
#include <set>
#include <vector>

using std::priority_queue;
using std::set;
using std::vector;
using std::greater;

class Solution {
  Status init;
  Status target;
  struct cmp {
    bool operator()(Status *&a, Status *&b) {
      return *b < *a;
    }
  };
  struct myLess {
    bool operator()(const Status &a,const Status &b) {
      return a.lessThan(b);
    }
  };
  priority_queue<Status *, vector<Status *>, cmp> explore;
  set<Status *> explored_pop;
  set<Status, myLess> visited;
public:
  Solution() = delete;
  Solution(const Status &node1, const Status &node2);
  ~Solution();
  list<Status *> AStarSolution();
};

#endif