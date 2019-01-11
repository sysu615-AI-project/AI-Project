#ifndef _STATUS_HPP_
#define _STATUS_HPP_

#include <iostream>
#include <list>
#define ROW 3
#define COL 3
#define N 9
using std::ostream;
using std::list;
enum Action {MoveTop = 0, MoveRight, MoveDown, MoveLeft};

class Status {
  int nums[N];
  int positionOf0;
  int estimatedValue;
  Status *parent;
public:
  Status();
  Status(const Status &);
  Status(const Status &, Status *p);
  Status(const int *nums, Status *p);

  int operator^(const Status &) const;
  bool operator==(const Status &) const;
  bool operator<(const Status &) const;
  bool lessThan(const Status &) const;
  // Status &operator=(const Status &);
  bool move(Action act);
  void setEstimatedValue(int e);
  list<Status *> getPath();
  friend ostream &operator<<(ostream &os, const Status &s);
};

#endif