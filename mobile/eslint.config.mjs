/**
 * ESLint configuration for a React Native app
 * Save this as eslint.config.mjs
 */
export default [
  {
    files: ['**/*.js', '**/*.jsx', '**/*.ts', '**/*.tsx'],
    ignores: ['node_modules', 'dist', 'build'],
    languageOptions: {
      ecmaVersion: 2021,
      sourceType: 'module',
      globals: {
        __DEV__: 'readonly',
        fetch: 'readonly',
        require: 'readonly',
      },
    },
    plugins: {
      react: require('eslint-plugin-react'),
      'react-native': require('eslint-plugin-react-native'),
    },
    rules: {
      'react/jsx-uses-react': 'off',
      'react/react-in-jsx-scope': 'off',
      'react/prop-types': 'off',
      'react-native/no-unused-styles': 'warn',
      'react-native/split-platform-components': 'warn',
      'react-native/no-inline-styles': 'warn',
      'react-native/no-color-literals': 'off',
      'react-native/no-raw-text': 'off',
    },
    settings: {
      react: {
        version: 'detect',
      },
    },
  },
];
