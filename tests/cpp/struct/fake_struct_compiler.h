#include "taichi/struct/struct.h"

namespace taichi::lang {

class FakeStructCompiler : public StructCompiler {
 public:
  void generate_types(SNode &) override {
  }

  void generate_child_accessors(SNode &) override {
  }

  void run(SNode &root) override {
  }
};

}  // namespace taichi::lang
