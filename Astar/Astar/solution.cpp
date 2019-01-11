#include "solution.hpp"
Solution::Solution(const Status &node1, const Status &node2) {
  init = node1;
  target = node2;
}

list<Status *> Solution::AStarSolution() {
  list<Status *> l;
  Status *p = new Status(init), *ptemp = NULL;
  explore.push(p);
  visited.insert(*p);
  explored_pop.insert(p);
  bool canMove;
  while (explore.size()) {
    p = explore.top();
    visited.insert(*p);
    explored_pop.insert(p);
    explore.pop();

    if (*p == target) {
      return p->getPath();
    }
    for (int i = 0; i < 4; ++i) {
      ptemp = new Status(*p, p);
      canMove = ptemp->move((Action) i);
      if (canMove && visited.find(*ptemp) == visited.end()) {
        ptemp->setEstimatedValue((*ptemp) ^ target);
        explore.push(ptemp);
      } else {
        delete ptemp;
      }
    }
  }
  return l;
}

Solution::~Solution() {
  Status *p;
  while (explore.size()) {
    p = explore.top();
    delete p;
    explore.pop();
  }
  for (auto &s:explored_pop) {
    delete s;
  }
}