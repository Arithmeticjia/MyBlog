<template>
  <div class="tree">
    <div class="tree-list">
      <node-tree :node="treeData"></node-tree>
    </div>
    <el-divider></el-divider>
  </div>
</template>

<script>
import NodeTree from "./NodeTree";
export default {
  name: "Tree",
  props: {
    treeData: Object
  },
  components: {
    NodeTree
  }
}
</script>

<style scoped>

</style>
