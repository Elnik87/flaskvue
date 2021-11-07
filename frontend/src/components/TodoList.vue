<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Список дел</h1>
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.todo-modal>Добавить запись</button>
        <br><br>
        <table class="table table-hover">
          <thead>
          <tr>
            <th scope="col">Задача</th>
            <th scope="col">Кто поставил</th>
            <th scope="col">Важная</th>
            <th></th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(todo, index) in todos" :key="index">
            <td>{{ todo.content }}</td>
            <td>{{ todo.boss }}</td>
            <td>
              <span v-if="todo.important">Важная</span>
              <span v-else>-</span>
            </td>
            <td>
              <div class="btn-group" role="group">
                <button
                  type="button"
                  class="btn btn-warning btn-sm"
                  v-b-modal.todo-update-modal
                  @click="editTodo(todo)">
                  Обновить
                </button>
                <button
                  type="button"
                  class="btn btn-danger btn-sm"
                  @click="onDeleteTodo(todo)">
                  Удалить
                </button>
              </div>
            </td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addTodoModal"
             id="todo-modal"
             title="Добавить новую задачу"
             hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-content-group"
                      label="Задача:"
                      label-for="form-title-input">
          <b-form-input id="form-content-input"
                        type="text"
                        v-model="addTodoForm.content"
                        required
                        placeholder="Записать задачу">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-boss-group"
                      label="Кто поставил задачу:"
                      label-for="form-boss-input">
          <b-form-input id="form-boss-input"
                        type="text"
                        v-model="addTodoForm.boss"
                        required
                        placeholder="Фамилия начальника, кто поставил задачу">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-important-group">
          <b-form-checkbox-group v-model="addTodoForm.important" id="form-checks">
            <b-form-checkbox value="true">Важная задача?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Добавить</b-button>
          <b-button type="reset" variant="danger">Отменить</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
    <b-modal ref="editTodoModal"
             id="todo-update-modal"
             title="Обновить"
             hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
        <b-form-group id="form-content-edit-group"
                      label="Добавить задачу:"
                      label-for="form-title-edit-input">
          <b-form-input id="form-content-edit-input"
                        type="text"
                        v-model="editForm.content"
                        required
                        placeholder="Здесь записать задачу">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-boss-edit-group"
                      label="Начальник, поставивший задачу:"
                      label-for="form-boss-edit-input">
          <b-form-input id="form-boss-edit-input"
                        type="text"
                        v-model="editForm.boss"
                        required
                        placeholder="Фамилия начальника, поставившего задачу">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-important-edit-group">
          <b-form-checkbox-group v-model="editForm.important" id="form-checks">
            <b-form-checkbox value="true">Важная задача?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Обновить</b-button>
          <b-button type="reset" variant="danger">Отмена</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './NewDo.vue';

export default {
  data() {
    return {
      todos: [],
      addTodoForm: {
        content: '',
        boss: '',
        important: [],
      },
      message: '',
      showMessage: false,
      editForm: {
        id: '',
        content: '',
        boss: '',
        important: [],
      },
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getTodos() {
      const path = 'http://localhost:5000/todos'; // получаем список дел из flask
      axios.get(path)
        .then((res) => {
          this.todos = res.data.todos;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addTodo(payload) {
      const path = 'http://localhost:5000/todos'; // отправляем список дел в flask
      axios.post(path, payload)
        .then(() => {
          this.getTodos();
          this.message = 'Задача добавлена';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getTodos();
        });
    },
    initForm() {
      this.addTodoForm.content = '';
      this.addTodoForm.boss = '';
      this.addTodoForm.important = [];
      this.editForm.id = '';
      this.editForm.content = '';
      this.editForm.boss = '';
      this.editForm.important = [];
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addTodoModal.hide();
      let important = false;
      if (this.addTodoForm.important[0]) important = true;
      const payload = {
        content: this.addTodoForm.content,
        boss: this.addTodoForm.boss,
        important, // галочка про важность
      };
      this.addTodo(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addTodoModal.hide();
      this.initForm();
    },
    editTodo(todo) {
      this.editForm = todo;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editTodoModal.hide();
      let important = false;
      if (this.editForm.important[0]) important = true;
      const payload = {
        content: this.editForm.content,
        boss: this.editForm.boss,
        important,
      };
      this.updateTodo(payload, this.editForm.id);
    },
    updateTodo(payload, todoID) {
      const path = `http://localhost:5000/todos/${todoID}`;
      axios.put(path, payload)
        .then(() => {
          this.getTodos();
          this.message = 'Задача обновлена';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getTodos();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editTodoModal.hide();
      this.initForm();
      this.getTodos();
    },
    removeTodo(todoID) {
      const path = `http://localhost:5000/todos/${todoID}`; // удалить из flask одну задачу по id
      axios.delete(path)
        .then(() => {
          this.getTodos();
          this.message = 'Задача удалена';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getTodos();
        });
    },
    onDeleteTodo(todo) {
      this.removeTodo(todo.id);
    },
  },
  created() {
    this.getTodos();
  },
};
</script>
