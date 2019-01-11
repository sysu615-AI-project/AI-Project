#include "status.hpp"
#include <cmath>

Status::Status() {}

Status::Status(const Status &other) {
  for (int i = 0; i < N; ++i) {
    nums[i] = other.nums[i];
  }
  positionOf0 = other.positionOf0;
  estimatedValue = other.positionOf0;
  parent = other.parent;
}
Status::Status(const Status &other, Status *p) {
  for (int i = 0; i < N; ++i) {
    nums[i] = other.nums[i];
  }
  positionOf0 = other.positionOf0;
  estimatedValue = other.positionOf0;
  parent = p;
}
Status::Status(const int *_nums, Status *p) {
  for (int i = 0; i < N; ++i) {
    nums[i] = _nums[i];
    if (nums[i] == 0) {
      positionOf0 = i;
    }
  }
  estimatedValue = 0;
  parent = p;
}

int Status::operator^(const Status &other) const {
  int count = 0;
  for (int i = 0; i < N; ++i) {
    if (nums[i] != other.nums[i]) {
      count = count + 1;
      int j;
      for (j = 0; j < N; ++j) {
        if (nums[i] == other.nums[j]) {
          break;
        }
      }
      count = count + abs(i % 3 - j % 3) + abs(i / 3 - j / 3);
    }
  }
  return count;
}

bool Status::operator<(const Status &other) const {
  return estimatedValue < other.estimatedValue;
}
bool Status::lessThan(const Status &other) const {
  for (int i = 0; i < N; ++i) {
    if (nums[i] < other.nums[i]) {
      return true;
    } else if (nums[i] > other.nums[i]) {
      return false;
    }
  }
  return false;
}

bool Status::operator==(const Status &other) const {
  if (positionOf0 != other.positionOf0) return false;
  for (int i = 0; i < N; ++i) {
    if (nums[i] != other.nums[i]) {
      return false;
    }
  }
  return true;
}

bool Status::move(Action act) {
  switch(act) {
    case MoveTop:
      if (positionOf0 >= COL) {
        nums[positionOf0] = nums[positionOf0 - COL];
        positionOf0 = positionOf0 - COL;
        nums[positionOf0] = 0;
        return true;
      }
      break;
    case MoveRight:
      if (positionOf0 % COL < COL - 1) {
        nums[positionOf0] = nums[positionOf0 + 1];
        positionOf0 = positionOf0 + 1;
        nums[positionOf0] = 0;
        return true;
      }
      break;
    case MoveDown:
      if (positionOf0 + COL < N) {
        nums[positionOf0] = nums[positionOf0 + COL];
        positionOf0 = positionOf0 + COL;
        nums[positionOf0] = 0;
        return true;
      }
      break;
    case MoveLeft:
      if (positionOf0 % COL) {
        nums[positionOf0] = nums[positionOf0 - 1];
        positionOf0 = positionOf0 - 1;
        nums[positionOf0] = 0;
        return true;
      }
      break;
  }
  return false;
}

void Status::setEstimatedValue(int e) {
  estimatedValue = e;
}

list<Status *> Status::getPath() {
  list<Status *> l;
  l.push_front(this);
  Status *p = this;
  while (p->parent) {
    l.push_front(p->parent);
    p = p->parent;
  }
  return l;
}


ostream &operator<<(ostream &os, const Status &s) {
  os << '[';
  for (int i = 0; i < N - 1; ++i) {
    os << s.nums[i] << ", ";
  }
  os << s.nums[N - 1] << ']';
  return os;
}