import { Text, View } from 'react-native';
import { Link } from 'expo-router';
export default function HomeScreen() {
  return (
    <View
      style={{
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        height: '100%',
      }}
    >
      <Text
        style={{
          fontSize: 20,
          fontWeight: 'bold',
          margin: 'auto',
        }}
      >
        Home
      </Text>
      <Link href="/">View details</Link>
    </View>
  );
}
