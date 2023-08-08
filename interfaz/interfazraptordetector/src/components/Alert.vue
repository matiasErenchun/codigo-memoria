<template>
  <div class="alert" :class="type">
    {{ message }}
  </div>
</template>

<script>
export default {
  props: {
    show: Boolean,
    type: String,
    message: String
  }
};
</script>

<style scoped>
.alert {
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-bottom: 10px;
}

.success {
  background-color: #d4edda;
  border-color: #c3e6cb;
  color: #155724;
}

.error {
  background-color: #f8d7da;
  border-color: #f5c6cb;
  color: #721c24;
}
</style>
