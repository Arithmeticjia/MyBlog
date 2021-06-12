<template>
  <li class="comment-item" >
        <div class="comments-content">
            <div class="post__author author vcard">
                <div class="author-date">
                    <a class="h6 post__author-name fn" href="#">{{node.user}}</a>
                    <div class="post__date">
                        <time class="published" datetime="node.created_at">
                            &nbsp; -  {{node.created_time}}
                        </time>
                    </div>
                </div>
            </div>
            <p>{{node.body}}</p>
            <a href="#" class="reply">Reply</a>
            <a href="#" class="report">Report</a>
        </div>
  </li>
</template>

<script>
export default {
  name: "node",
  props: {
    node: Object
  }
};
</script>

<style scoped>

</style>
