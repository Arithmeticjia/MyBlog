<template>
  <div class="tree">
    <ul class="tree-list">
      <node-tree :node="treeData"></node-tree>
    </ul>
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
