<template>
  <div class="star-rating" :class="{ readonly: readonly }">
    <button
      v-for="star in 5"
      :key="star"
      type="button"
      class="star"
      :class="{ active: star <= (hoverRating || currentRating) }"
      @click="!readonly && setRating(star)"
      @mouseenter="!readonly && (hoverRating = star)"
      @mouseleave="!readonly && (hoverRating = 0)"
      :disabled="readonly"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        :fill="star <= (hoverRating || currentRating) ? 'currentColor' : 'none'"
        stroke="currentColor"
        stroke-width="2"
      >
        <path
          d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"
        />
      </svg>
    </button>
    <span v-if="showLabel" class="rating-label">
      {{ currentRating === 0 ? 'امتیاز دهید' : `${currentRating} از 5` }}
    </span>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: Number,
    default: 0
  },
  readonly: {
    type: Boolean,
    default: false
  },
  showLabel: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:modelValue'])

const currentRating = ref(props.modelValue)
const hoverRating = ref(0)

const setRating = (rating) => {
  currentRating.value = rating
  emit('update:modelValue', rating)
}

watch(() => props.modelValue, (newValue) => {
  currentRating.value = newValue
})
</script>

<style scoped>
.star-rating {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  direction: ltr;
}

.star {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  width: 28px;
  height: 28px;
  transition: all 0.2s ease;
}

.star:not(:disabled):hover {
  transform: scale(1.1);
}

.star.active {
  color: #fbbf24;
}

.star:not(.active) {
  color: #d1d5db;
}

.star.readonly,
.readonly .star {
  cursor: default;
  pointer-events: none;
}

.star svg {
  width: 100%;
  height: 100%;
  display: block;
}

.rating-label {
  margin-right: 0.5rem;
  font-size: 0.875rem;
  color: #6b7280;
  white-space: nowrap;
  direction: rtl;
}

@media (max-width: 640px) {
  .star {
    width: 24px;
    height: 24px;
  }
  
  .rating-label {
    font-size: 0.8rem;
  }
}
</style>
