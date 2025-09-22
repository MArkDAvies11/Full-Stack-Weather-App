import React from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';

const UserSchema = Yup.object().shape({
  username: Yup.string()
    .min(3, 'Username must be at least 3 characters')
    .max(20, 'Username must be less than 20 characters')
    .required('Username is required'),
  email: Yup.string()
    .email('Invalid email format')
    .required('Email is required')
});

function UserForm({ onSubmit, editingUser, onCancel }) {
  return (
    <Formik
      initialValues={{
        username: editingUser?.username || '',
        email: editingUser?.email || ''
      }}
      validationSchema={UserSchema}
      onSubmit={onSubmit}
      enableReinitialize
    >
      <Form className="user-form">
        <div className="form-group">
          <Field
            type="text"
            name="username"
            placeholder="Username"
            className="form-input"
          />
          <ErrorMessage name="username" component="div" className="error" />
        </div>

        <div className="form-group">
          <Field
            type="email"
            name="email"
            placeholder="Email"
            className="form-input"
          />
          <ErrorMessage name="email" component="div" className="error" />
        </div>

        <button type="submit" className="form-button">
          {editingUser ? 'Update User' : 'Add User'}
        </button>
        
        {editingUser && (
          <button type="button" onClick={onCancel} className="cancel-button">
            Cancel
          </button>
        )}
      </Form>
    </Formik>
  );
}

export default UserForm;