<template>
  <div class="editor">
    <div class="menubar">
      <span v-for="actionName in activeButtons" :key="actionName">
        <button
          v-if="actionName === 'bold'"
          class="menubar__button"
          :class="{ 'is-active': editor.isActive('bold') }"
          @click="editor.chain().focus().toggleBold().run()"
        >
          <icon name="bold" />
        </button>
        <button
          v-if="actionName === 'italic'"
          class="menubar__button"
          :class="{ 'is-active': editor.isActive('italic') }"
          @click="editor.chain().focus().toggleItalic().run()"
        >
          <icon name="italic" />
        </button>

        <button
          v-if="actionName === 'strike'"
          class="menubar__button"
          :class="{ 'is-active': editor.isActive('strike') }"
          @click="editor.chain().focus().toggleStrike().run()"
        >
          <icon name="strike" />
        </button>

        <button
          v-if="actionName === 'underline'"
          class="menubar__button"
          :class="{ 'is-active': editor.isActive('underline') }"
          @click="editor.chain().focus().toggleUnderline().run()"
        >
          <icon name="underline" />
        </button>

        <button
          v-if="actionName === 'code'"
          class="menubar__button"
          :class="{ 'is-active': editor.isActive('code') }"
          @click="editor.chain().focus().toggleCode().run()"
        >
          <icon name="code" />
        </button>

        <button
          v-if="actionName === 'h1'"
          class="menubar__button"
          :class="{ 'is-active': editor.isActive('heading', { level: 1 }) }"
          @click="editor.chain().focus().toggleHeading({ level: 1 }).run()"
        >
          H1
        </button>

        <button
          v-if="actionName === 'h2'"
          class="menubar__button"
          :class="{ 'is-active': editor.isActive('heading', { level: 2 }) }"
          @click="editor.chain().focus().toggleHeading({ level: 2 }).run()"
        >
          H2
        </button>

        <button
          v-if="actionName === 'h3'"
          class="menubar__button"
          :class="{ 'is-active': editor.isActive('heading', { level: 3 }) }"
          @click="editor.chain().focus().toggleHeading({ level: 3 }).run()"
        >
          H3
        </button>

        <button
          v-if="actionName === 'bulletList'"
          class="menubar__button"
          :class="{ 'is-active': editor.isActive('bulletList') }"
          @click="editor.chain().focus().toggleBulletList().run()"
        >
          <icon name="ul" />
        </button>

        <button
          v-if="actionName === 'orderedList'"
          class="menubar__button"
          :class="{ 'is-active': editor.isActive('orderedList') }"
          @click="editor.chain().focus().toggleOrderedList().run()"
        >
          <icon name="ol" />
        </button>

        <button
          v-if="actionName === 'blockquote'"
          class="menubar__button"
          :class="{ 'is-active': editor.isActive('blockquote') }"
          @click="editor.chain().focus().toggleBlockquote().run()"
        >
          <icon name="quote" />
        </button>

        <button
          v-if="actionName === 'codeBlock'"
          class="menubar__button"
          :class="{ 'is-active': editor.isActive('codeBlock') }"
          @click="editor.chain().focus().toggleCodeBlock().run()"
        >
          <icon name="code" />
        </button>

        <button
          v-if="actionName === 'horizontalRule'"
          class="menubar__button"
          @click="editor.chain().focus().setHorizontalRule().run()"
        >
          <icon name="hr" />
        </button>

        <button
          v-if="actionName === 'undo'"
          class="menubar__button"
          @click="editor.chain().focus().undo().run()"
        >
          <icon name="undo" />
        </button>

        <button
          v-if="actionName === 'redo'"
          class="menubar__button"
          @click="editor.chain().focus().redo().run()"
        >
          <icon name="redo" />
        </button>

        <button
          v-if="actionName === 'image'"
          class="menubar__button"
          @click="addImage"
          title="插入图片"
        >
          <icon name="image" />
        </button>
      </span>
      <button class="menubar__button" title="插入手写画布" @click="openDrawModal">✍️</button>
      <button class="menubar__button" title="添加文字块" @click="insertTextBlock">添加文字</button>
      <button class="menubar__button" title="插入可拖拽文本框" @click="insertDraggableBlock">文本框</button>
      <button class="menubar__button" title="插入可拖拽图片块" @click="insertDraggableImageBlock">图片框</button>
    </div>

    <!-- Image URL input modal -->
    <div
      v-if="showImageModal"
      class="image-modal-overlay"
      @click="closeImageModal"
    >
      <div class="image-modal" @click.stop>
        <h4>插入图片</h4>
        <input
          v-model="imageUrl"
          type="url"
          placeholder="输入图片链接..."
          class="image-url-input"
          @keyup.enter="insertImage"
        />
        <div class="modal-buttons">
          <button @click="insertImage" class="insert-btn">插入</button>
          <button @click="closeImageModal" class="cancel-btn">取消</button>
        </div>
      </div>
    </div>

    <div
      v-if="showDrawModal"
      class="image-modal-overlay"
      @click="closeDrawModal"
    >
      <div class="image-modal" @click.stop>
        <h4>手写画布</h4>
        <div style="display:flex; gap:8px; margin-bottom:8px; align-items:center;">
          <label>颜色: <input type="color" v-model="drawColor" /></label>
          <label>线宽: <input type="range" min="1" max="8" v-model="lineWidth" /></label>
          <button @click="saveDrawing" class="insert-btn">保存为图片</button>
          <button @click="closeDrawModal" class="cancel-btn">取消</button>
        </div>
        <canvas
          ref="drawCanvas"
          width="600"
          height="320"
          style="width:100%; border:1px solid #ccc; touch-action:none;"
          @pointerdown="startDrawing"
          @pointermove="drawPointer"
          @pointerup="stopDrawing"
          @pointerleave="stopDrawing"
        ></canvas>
      </div>
    </div>

    <div class="canvas-board">
      <div class="canvas-hint">这是手账画布区域，工具栏可以添加文字/手写/图片块后拖拽排版。</div>
      <editor-content class="editor__content" :editor="editor" />
    </div>
  </div>
</template>

<script>
import Icon from './Icon.vue';
import { Editor, EditorContent, VueNodeViewRenderer } from '@tiptap/vue-3';
import StarterKit from '@tiptap/starter-kit';
import Underline from '@tiptap/extension-underline';
import Image from '@tiptap/extension-image';
import { Node, mergeAttributes } from '@tiptap/core';
import { defineComponent, ref, onMounted, onBeforeUnmount } from 'vue';

const DraggableBlockNodeView = defineComponent({
  props: ['node', 'updateAttributes', 'editor', 'getPos'],
  setup(props) {
    const drag = ref(false);
    const resize = ref(false);
    const start = ref({ x: 0, y: 0 });
    const size = ref({ width: props.node.attrs.width || 320, height: props.node.attrs.height || 140 });
    const pos = ref({ x: props.node.attrs.x || 20, y: props.node.attrs.y || 20 });

    const blockStyle = ref({
      left: `${pos.value.x}px`,
      top: `${pos.value.y}px`,
      width: `${size.value.width}px`,
      height: `${size.value.height}px`,
    });

    const updateAttrs = () => {
      props.updateAttributes({ x: pos.value.x, y: pos.value.y, width: size.value.width, height: size.value.height });
      blockStyle.value = {
        left: `${pos.value.x}px`,
        top: `${pos.value.y}px`,
        width: `${size.value.width}px`,
        height: `${size.value.height}px`,
      };
    };

    const onHandleDown = (event) => {
      event.preventDefault();
      drag.value = true;
      start.value = {
        x: event.clientX,
        y: event.clientY,
        startX: pos.value.x,
        startY: pos.value.y,
      };
      window.addEventListener('pointermove', onDragMove);
      window.addEventListener('pointerup', onStop);
    };

    const onResizeDown = (event) => {
      event.preventDefault();
      resize.value = true;
      start.value = {
        x: event.clientX,
        y: event.clientY,
        startW: size.value.width,
        startH: size.value.height,
      };
      window.addEventListener('pointermove', onResizeMove);
      window.addEventListener('pointerup', onStop);
    };

    const onDragMove = (event) => {
      if (!drag.value) return;
      const dx = event.clientX - start.value.x;
      const dy = event.clientY - start.value.y;
      pos.value.x = Math.max(0, start.value.startX + dx);
      pos.value.y = Math.max(0, start.value.startY + dy);
      updateAttrs();
    };

    const onResizeMove = (event) => {
      if (!resize.value) return;
      const dx = event.clientX - start.value.x;
      const dy = event.clientY - start.value.y;
      size.value.width = Math.max(150, start.value.startW + dx);
      size.value.height = Math.max(80, start.value.startH + dy);
      updateAttrs();
    };

    const onStop = () => {
      drag.value = false;
      resize.value = false;
      window.removeEventListener('pointermove', onDragMove);
      window.removeEventListener('pointermove', onResizeMove);
      window.removeEventListener('pointerup', onStop);
    };

    onBeforeUnmount(() => {
      window.removeEventListener('pointermove', onDragMove);
      window.removeEventListener('pointermove', onResizeMove);
      window.removeEventListener('pointerup', onStop);
    });

    return {
      blockStyle,
      onHandleDown,
      onResizeDown,
    };
  },
  template: `
    <div class="draggable-block" :style="blockStyle">
      <div class="block-handle" @pointerdown.prevent="onHandleDown">↕ 拖拽</div>
      <div class="block-resize" @pointerdown.prevent="onResizeDown">↔</div>
      <div class="block-content" data-node-view-content></div>
    </div>
  `,
});

const DraggableBlock = Node.create({
  name: 'draggableBlock',
  group: 'block',
  content: 'inline*',
  draggable: true,
  selectable: true,
  addAttributes() {
    return {
      x: { default: 20 },
      y: { default: 20 },
      width: { default: 320 },
      height: { default: 140 },
    };
  },
  parseHTML() {
    return [{ tag: 'div[data-type="draggable-block"]' }];
  },
  renderHTML({ node, HTMLAttributes }) {
    const style = `position:absolute; left:${node.attrs.x}px; top:${node.attrs.y}px; width:${node.attrs.width}px; height:${node.attrs.height}px;`;
    return ['div', mergeAttributes({ 'data-type': 'draggable-block', style }, HTMLAttributes), 0];
  },
  addNodeView() {
    return VueNodeViewRenderer(DraggableBlockNodeView);
  },
});

export default {
  name: 'Editor',
  components: {
    EditorContent,
    Icon,
  },
  props: {
    initialContent: {
      type: String,
      required: true,
      default: '<em>editable text</em>',
    },
    placeholder: {
      type: String,
      default: '',
    },
    activeButtons: {
      type: Array,
      validator: function (list) {
        for (let el of list) {
          // The value must match one of these strings
          if (
            [
              'bold',
              'italic',
              'strike',
              'underline',
              'code',
              'h1',
              'h2',
              'h3',
              'bulletList',
              'orderedList',
              'blockquote',
              'codeBlock',
              'horizontalRule',
              'undo',
              'redo',
              'image',
            ].indexOf(el) === -1
          ) {
            return -1;
          }
        }
        return 1;
      },
      default: () => ['bold', 'italic'],
    },
  },
  emits: ['update'],
  data() {
    return {
      html: '',
      json: '',
      editor: null,
      showImageModal: false,
      imageUrl: '',
      showDrawModal: false,
      isDrawing: false,
      drawColor: '#222',
      lineWidth: 2,
      drawPath: [],
    };
  },
  created() {
    this.editor = new Editor({
      content: this.initialContent,
      editorProps: {
        attributes: {
          placeholder: this.placeholder,
        },
      },
      extensions: [
        StarterKit,
        Underline,
        Image.configure({
          HTMLAttributes: {
            class: 'editor-image',
          },
        }),
        DraggableBlock,
      ],
    });

    this.html = this.editor.getHTML();
    this.json = this.editor.getJSON();

    this.editor.on('update', () => {
      this.html = this.editor.getHTML();
      this.json = this.editor.getJSON();
      this.$emit('update', this.html);
    });
  },
  beforeUnmount() {
    this.editor.destroy();
  },
  methods: {
    addImage() {
      this.showImageModal = true;
      this.imageUrl = '';
    },
    closeImageModal() {
      this.showImageModal = false;
      this.imageUrl = '';
    },
    insertImage() {
      if (this.imageUrl.trim()) {
        this.editor.chain().focus().setImage({ src: this.imageUrl }).run();
        this.closeImageModal();
      }
    },
    openDrawModal() {
      this.showDrawModal = true;
      this.$nextTick(() => {
        const canvas = this.$refs.drawCanvas;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        ctx.fillStyle = '#fff';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
      });
    },
    closeDrawModal() {
      this.showDrawModal = false;
      this.isDrawing = false;
      this.drawPath = [];
    },
    startDrawing(event) {
      const canvas = this.$refs.drawCanvas;
      if (!canvas) return;
      const rect = canvas.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;
      this.isDrawing = true;
      this.drawPath = [{ x, y }];
      const ctx = canvas.getContext('2d');
      ctx.strokeStyle = this.drawColor;
      ctx.lineWidth = this.lineWidth;
      ctx.beginPath();
      ctx.moveTo(x, y);
    },
    drawPointer(event) {
      if (!this.isDrawing) return;
      const canvas = this.$refs.drawCanvas;
      const rect = canvas.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;
      this.drawPath.push({ x, y });
      const ctx = canvas.getContext('2d');
      ctx.lineTo(x, y);
      ctx.stroke();
    },
    stopDrawing() {
      this.isDrawing = false;
    },
    saveDrawing() {
      const canvas = this.$refs.drawCanvas;
      const pngUrl = canvas.toDataURL('image/png');
      this.editor.chain().focus().setImage({ src: pngUrl }).run();
      this.closeDrawModal();
    },
    insertDraggableBlock() {
      this.editor.chain().focus().insertContent({
        type: 'draggableBlock',
        attrs: {
          x: 20,
          y: 20,
          width: 360,
          height: 160,
        },
        content: [
          {
            type: 'text',
            text: '在这里输入自由排版文本...可以拖拽、调整大小',
          },
        ],
      }).run();
    },
    insertTextBlock() {
      const text = window.prompt('输入文本块内容', '手账文字');
      if (!text) return;
      this.editor.chain().focus().insertContent({
        type: 'draggableBlock',
        attrs: { x: 30, y: 30, width: 320, height: 120 },
        content: [{ type: 'text', text }],
      }).run();
    },
    insertDraggableImageBlock() {
      const url = window.prompt('输入图片地址');
      if (!url) return;
      this.editor.chain().focus().insertContent({
        type: 'draggableBlock',
        attrs: {
          x: 40,
          y: 40,
          width: 320,
          height: 220,
        },
        content: [
          {
            type: 'text',
            text: '图片块：',
          },
          {
            type: 'image',
            attrs: {
              src: url,
              alt: '自由图像',
            },
          },
        ],
      }).run();
    },
  },
};
</script>

<style lang="css" scoped>
.editor {
  border: 1px solid #ccc;
  border-radius: 4px;
  overflow: hidden;
}

.menubar {
  display: flex;
  flex-wrap: wrap;
  padding: 0.5rem;
  border-bottom: 1px solid #ccc;
  background: #f8f9fa;
}

.menubar__button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  margin: 0.1rem;
  border: none;
  background: transparent;
  border-radius: 0.3rem;
  color: #333;
  cursor: pointer;
  font-size: 0.8rem;
  transition: all 0.2s;
}

.menubar__button:hover {
  background: #e9ecef;
}

.menubar__button.is-active {
  background: #007bff;
  color: white;
}

.editor__content {
  padding: 12px;
  min-height: 540px;
  outline: none;
  background: #fefcf5;
  border: 2px dashed #d0b46c;
  border-radius: 8px;
  box-shadow: inset 0 0 0 1px #f5e2ab;
}

/* Image Modal Styles */
.image-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.image-modal {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.image-modal h4 {
  margin: 0 0 15px 0;
  color: #333;
}

.image-url-input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  margin-bottom: 15px;
  box-sizing: border-box;
}

.modal-buttons {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.insert-btn,
.cancel-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.insert-btn {
  background: #28a745;
  color: white;
}

.insert-btn:hover {
  background: #218838;
}

.cancel-btn {
  background: #6c757d;
  color: white;
}

.draw-canvas {
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 5px;
  background: #fff;
}

:deep(.ProseMirror) {
  outline: none;
  min-height: 200px;
}

:deep(.ProseMirror h1) {
  font-size: 2em;
  font-weight: bold;
  margin: 0.5em 0;
}

:deep(.ProseMirror h2) {
  font-size: 1.5em;
  font-weight: bold;
  margin: 0.5em 0;
}

:deep(.ProseMirror h3) {
  font-size: 1.25em;
  font-weight: bold;
  margin: 0.5em 0;
}

:deep(.ProseMirror blockquote) {
  border-left: 4px solid #ddd;
  padding-left: 1em;
  margin: 1em 0;
  color: #666;
  font-style: italic;
}

:deep(.ProseMirror ul) {
  padding-left: 2em;
}

:deep(.ProseMirror ol) {
  padding-left: 2em;
}

:deep(.ProseMirror code) {
  background: #f4f4f4;
  padding: 2px 4px;
  border-radius: 3px;
  font-family: monospace;
}

:deep(.ProseMirror pre) {
  background: #f4f4f4;
  padding: 1em;
  border-radius: 4px;
  overflow-x: auto;
}

:deep(.ProseMirror pre code) {
  background: none;
  padding: 0;
}

.canvas-board {
  position: relative;
  width: 100%;
  min-height: 620px;
  background: #fefdf5;
  border: 2px dashed #c8b17a;
  border-radius: 8px;
  padding: 12px;
  box-sizing: border-box;
}
.canvas-hint {
  font-size: 12px;
  color: #6f4c1f;
  margin-bottom: 8px;
}
.editor__content {
  position: relative;
  min-height: 520px;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 6px;
  padding: 8px;
  box-sizing: border-box;
  overflow: hidden;
}

.draggable-block {
  position: absolute;
  border: 1px dashed #8888;
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 2px 7px rgba(0,0,0,0.15);
  border-radius: 6px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
.draggable-block .block-handle {
  cursor: grab;
  background: #f0f0f0;
  border-bottom: 1px solid #ddd;
  padding: 4px 8px;
  font-size: 12px;
  color: #333;
  user-select: none;
}
.draggable-block .block-content {
  flex: 1;
  min-height: 80px;
  padding: 8px;
  outline: none;
  white-space: normal;
}
.draggable-block .block-resize {
  width: 16px;
  height: 16px;
  position: absolute;
  right: 2px;
  bottom: 2px;
  background: #777;
  color: white;
  font-size: 10px;
  text-align: center;
  line-height: 16px;
  border-radius: 2px;
  cursor: nwse-resize;
}
</style>
