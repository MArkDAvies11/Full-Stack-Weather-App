import React from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';

const FavoriteSchema = Yup.object().shape({
  user_id: Yup.number()
    .positive('User ID must be positive')
    .integer('User ID must be an integer')
    .required('User ID is required'),
  city_name: Yup.string()
    .min(2, 'City name must be at least 2 characters')
    .required('City name is required')
});

function FavoriteForm({ onSubmit, users }) {
  return (
    <Formik
      initialValues={{
        user_id: '',
        city_name: ''
      }}
      validationSchema={FavoriteSchema}
      onSubmit={onSubmit}
    >
      <Form className="favorite-form">
        <div className="form-group">
          <Field as="select" name="user_id" className="form-input">
            <option value="">Select User</option>
            {users.map(user => (
              <option key={user.id} value={user.id}>
                {user.username}
              </option>
            ))}
          </Field>
          <ErrorMessage name="user_id" component="div" className="error" />
        </div>

        <div className="form-group">
          <Field
            type="text"
            name="city_name"
            placeholder="City Name"
            className="form-input"
          />
          <ErrorMessage name="city_name" component="div" className="error" />
        </div>

        <button type="submit" className="form-button">
          Add to Favorites
        </button>
      </Form>
    </Formik>
  );
}

export default FavoriteForm;