<script setup lang="ts">
// French letters at hand while typing an answer: the bar shows above the
// keyboard whenever a French text field (lang="fr") has focus.
import { computed, onBeforeUnmount, onMounted, ref } from 'vue';

const LETTERS = ['é', 'è', 'ê', 'à', 'â', 'ç', 'ù', 'û', 'î', 'ï', 'ô', 'ë', 'œ', '’', '«', '»'];

const field = ref<HTMLInputElement | HTMLTextAreaElement | null>(null);
const upper = ref(false);
const lift = ref(0); // px the on-screen keyboard covers at the bottom
const letters = computed(() => LETTERS.map((l) => (upper.value ? l.toLocaleUpperCase('fr') : l)));

const isFrench = (el: Element | null): el is HTMLInputElement | HTMLTextAreaElement =>
  (el instanceof HTMLTextAreaElement || (el instanceof HTMLInputElement && el.type === 'text')) &&
  el.closest('[lang="fr"]') !== null;

const onFocus = () => {
  const el = document.activeElement;
  field.value = isFrench(el) ? el : null;
};
// Focus moves to a letter button only for a moment: the button keeps it from leaving.
const onBlur = () => setTimeout(onFocus, 0);

const vv = window.visualViewport;
const onViewport = () => {
  if (vv) lift.value = Math.max(0, window.innerHeight - vv.height - vv.offsetTop);
};

onMounted(() => {
  document.addEventListener('focusin', onFocus);
  document.addEventListener('focusout', onBlur);
  vv?.addEventListener('resize', onViewport);
  vv?.addEventListener('scroll', onViewport);
});
onBeforeUnmount(() => {
  document.removeEventListener('focusin', onFocus);
  document.removeEventListener('focusout', onBlur);
  vv?.removeEventListener('resize', onViewport);
  vv?.removeEventListener('scroll', onViewport);
});

function insert(ch: string) {
  const el = field.value;
  if (!el) return;
  el.setRangeText(ch, el.selectionStart ?? el.value.length, el.selectionEnd ?? el.value.length, 'end');
  el.dispatchEvent(new Event('input', { bubbles: true }));
  upper.value = false;
}
</script>

<template>
  <div
    v-if="field"
    class="accent-bar"
    :class="{ 'is-lifted': lift > 0 }"
    :style="{ '--lift': lift + 'px' }"
    role="toolbar"
    aria-label="Французские буквы"
    @pointerdown.prevent
    @mousedown.prevent
  >
    <button type="button" class="accent-key accent-key--shift" :aria-pressed="upper" aria-label="Заглавные" @click="upper = !upper">⇧</button>
    <button v-for="l in letters" :key="l" type="button" class="accent-key" @click="insert(l)">{{ l }}</button>
  </div>
</template>
